# Calculates specific surface area (1/mm)

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt



id = 'FRE_20250122'
in_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/20250122/FRE_20250122_SSA.xlsx'

ssa = pd.read_excel(in_path, skiprows=3)


den = pd.read_csv('/Users/colemankane/Desktop/crrel_exports/FRE_20250122_den.csv')

table_path = 'lookUpTabFRED.txt'

table = np.genfromtxt(table_path, delimiter=',', skip_header=0, encoding='utf-8')

# A few checks to make sure that the density and ssa profiles are relatively coincident

den_avg = np.nanmean((den['A'], den['B'], den['C']), axis=0) / 1000 # calculate average densty at each height

ref_a = ssa['NIR %'] / 100

ref_b = ssa['NIR %.1']

ref_c = ssa['NIR %.2']

oed = table[:, ][0, 1:]
rho = table[:, ][1:, 0]
ref = table[:, ][1:, 1:]




# function to lookUp & interpolate the oed [um] or ssa [mm^-1] (=6/oed*1000) as implemented in the InfraSnow device
def interpolate_oed(rho_i, ref_i, k):
    ref_i = ref_i/k     # correction factor k = 1.09; 1.162; 1.119 as described in the manual
    l_rho = len(rho)
    l_oed = len(oed)

    # find rho's next neighbours
    for i in range(l_rho):
        if (rho_i - rho[i]) < 0:
            row2 = i
            row1 = i-1
            break
        if i == l_rho-1:
            row2 = i
            row1 = i-1

    # find OED values for nxt neighbour densities
    for i in range(l_oed):
        if (ref[row1, i] - ref_i) < 0:
            col_12 = i
            col_11 = i-1
            break
        elif i == l_oed-1:
            col_12 = l_oed
            col_11 = l_oed

    for i in range(l_oed):
        if (ref[row2, i] - ref_i) < 0:
            col_22 = i
            col_21 = i-1
            break
        if i == l_oed-1:
            col_22 = l_oed
            col_21 = l_oed

    # the 4 reflections from look-Up table to interpolate in between
    ref_11 = ref[row1, col_11]
    ref_12 = ref[row1, col_12]
    ref_21 = ref[row2, col_21]
    ref_22 = ref[row2, col_22]

    if (ref_12 - ref_11) == 0 or (ref_22 - ref_21) == 0:
        ssa = round(6 / max(oed) * 1000, 10)
        print ('measured reflectivity is smaller than range of the FRED model')

    # interpolated OED first inbetween reflectivities, then inbetween densities
    else:
        oedInt1 = oed[col_11] + abs(oed[col_12] - oed[col_11]) * (ref_i - ref_11) / (ref_12 - ref_11)
        oedInt2 = oed[col_21] + abs(oed[col_22] - oed[col_21]) * (ref_i - ref_21) / (ref_22 - ref_21)
        oedInt = oedInt2 - (oedInt2 - oedInt1) * (rho[row2] - rho_i) / (rho[row2] - rho[row1])
        ssa = round(6 / oedInt * 1000, 10)

    return ssa


cols = ['hag', 'density', 'reflect', 'ssa', 'oed']
conv_ssa = []
for i in range(len(ref_a)):
    conv_ssa.append([den['top'][i], den_avg[i], ref_a[i],
                     interpolate_oed(den_avg[i], ref_a[i], k=1.119),
                     6 / interpolate_oed(den_avg[i], ref_a[i], k=1.119)])

ssa_ar = pd.DataFrame(conv_ssa, columns=cols)
print(ssa_ar)

plt.scatter(ssa_ar['density'] * 100, ssa_ar['ssa'])
plt.show()
