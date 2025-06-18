# Calculates specific surface area (1/mm)

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt




def ssa_scrubber(ssa_path, id):
    '''
    Calculates specific surface area
    :param pit_path:
    :param id:
    :return:
    '''
    ssa_df = pd.read_excel(ssa_path, skiprows=3)
    print(id)
    if not ssa_df.empty:
        ssa_df.loc[ssa_df['SSA'].notna(), 'SSA'] = np.nan
        ssa_df.loc[ssa_df['SSA.1'].notna(), 'SSA.1'] = np.nan
        ssa_df.loc[ssa_df['SSA.2'].notna(), 'SSA.2'] = np.nan

        den_path = f'/Users/colemankane/Desktop/crrel_exports/{id}_den.csv'

        #try:
        den = pd.read_csv(den_path)

        table = np.genfromtxt('/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/lookUpTabFRED.txt', delimiter=',', skip_header=0, encoding='utf-8')
        # A few checks to make sure that the density and ssa profiles are relatively coincident

        den_avg = np.nanmean((den['A_kgm-3'], den['B_kgm-3'], den['C_kgm-3']),
                             axis=0) / 1000  # calculate average density at each height
        if id == 'DHMet_20250101':
            print(den_avg)
        ref_a = ssa_df['NIR %'] / 100

        ref_b = ssa_df['NIR %.1'] / 100

        ref_c = ssa_df['NIR %.2'] / 100

        def ix_cov(ssa_ix):
            hag = ssa_df.loc[ssa_ix, 'Height:\n(cm above ground)']
            if len(den_avg) >= len(ref_a):
                match = den[(den['top_cm'] >= hag) & (den['bottom_cm'] < hag)]
                return match.index
            else:
                if ssa_ix == len(ssa_df):
                    match = den_avg.tail(1)
                else:
                    match = den[(den['top_cm'] >= hag) & (den['bottom_cm'] < hag)]
                return match.index

        oed = table[:, ][0, 1:]
        rho = table[:, ][1:, 0]
        ref = table[:, ][1:, 1:]

        # function to lookUp & interpolate the oed [um] or ssa [mm^-1] (=6/oed*1000) as implemented in the InfraSnow device
        def interpolate_oed(rho_i, ref_i, k):
            ref_i = ref_i / k  # correction factor k = 1.09; 1.162; 1.119 as described in the manual
            l_rho = len(rho)
            l_oed = len(oed) - 1

            # find rho's next neighbours
            for i in range(l_rho):
                if (rho_i - rho[i]) < 0:
                    row2 = i
                    row1 = i - 1
                    break
                if i == l_rho - 1:
                    row2 = i
                    row1 = i - 1

            # find OED values for nxt neighbour densities
            for i in range(l_oed):
                if (ref[row1, i] - ref_i) < 0:
                    col_12 = i
                    col_11 = i - 1
                    break
                elif i == l_oed - 1:
                    col_12 = l_oed
                    col_11 = l_oed

            for i in range(l_oed):
                if (ref[row2, i] - ref_i) < 0:
                    col_22 = i
                    col_21 = i - 1
                    break
                if i == l_oed - 1:
                    col_22 = l_oed
                    col_21 = l_oed

            # the 4 reflections from look-Up table to interpolate in between
            ref_11 = ref[row1, col_11]
            ref_12 = ref[row1, col_12]
            ref_21 = ref[row2, col_21]
            ref_22 = ref[row2, col_22]

            if (ref_12 - ref_11) == 0 or (ref_22 - ref_21) == 0:
                ssa_val = round(6 / np.max(oed) * 1000, 1)

            # interpolated OED first inbetween reflectivities, then inbetween densities
            else:
                oedInt1 = oed[col_11] + abs(oed[col_12] - oed[col_11]) * (ref_i - ref_11) / (ref_12 - ref_11)
                oedInt2 = oed[col_21] + abs(oed[col_22] - oed[col_21]) * (ref_i - ref_21) / (ref_22 - ref_21)
                oedInt = float(oedInt2 - (oedInt2 - oedInt1) * (rho[row2] - rho_i) / (rho[row2] - rho[row1]))
                ssa_val = round(6 / oedInt * 1000, 1)

            return ssa_val

        cols = ['hag_cm', 'density_kgm-3', 'reflect_%', 'ssa_1/mm', 'oed_1_mm',
                'reflect2_%', 'ssa_2/mm', 'oed_2_mm',
                'reflect3_%', 'ssa_3/mm', 'oed_3_mm']
        #print(type(ref_a))
        conv_ssa = []
        for i in range(len(ref_a)):
            if i < len(den_avg):
                conv = ix_cov(i)
                conv_ssa.append(
                    [
                        ssa_df.loc[i, 'Height:\n(cm above ground)'],
                        float(den_avg[conv]) * 1000,
                        ref_a[i],
                        float(interpolate_oed(den_avg[conv], ref_a[i], k=1.119)),
                        6 / interpolate_oed(den_avg[conv], ref_a[i], k=1.119),
                        ref_b[i],
                        float(interpolate_oed(den_avg[conv], ref_b[i], k=1.119)),
                        6 / interpolate_oed(den_avg[conv], ref_b[i], k=1.119),
                        ref_c[i],
                        float(interpolate_oed(den_avg[conv], ref_c[i], k=1.119)),
                        6 / interpolate_oed(den_avg[conv], ref_c[i], k=1.119),
                    ]
                )

            else:
                conv = ix_cov(i)
                conv_ssa.append(
                    [ssa_df.loc[i, 'Height:\n(cm above ground)'],
                     float(den_avg[conv]) * 1000,
                     ref_a[i],
                     float(interpolate_oed(den_avg[conv], ref_a[i], k=1.119)),
                     6 / interpolate_oed(den_avg[conv], ref_a[i], k=1.119),
                     ref_b[i],
                     float(interpolate_oed(den_avg[conv], ref_b[i], k=1.119)),
                     6 / interpolate_oed(den_avg[conv], ref_b[i], k=1.119),
                     ref_c[i],
                     float(interpolate_oed(den_avg[conv], ref_c[i], k=1.119)),
                     6 / interpolate_oed(den_avg[conv], ref_c[i], k=1.119),
                     ]
                )


        ssa_ar = pd.DataFrame(conv_ssa, columns=cols)
        #ssa_ar = np.array(conv_ssa)

        ssa_ar.to_csv(f'/Users/colemankane/Desktop/crrel_exports/{id}_ssa.csv', index=False)
        print('file exported')



    else:
        pass



    return

"""
den = pd.read_csv(f'{id}_den.csv')

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
"""