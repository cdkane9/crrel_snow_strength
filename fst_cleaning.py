import pandas as pd
import matplotlib.pyplot as plt
from gap_fil_snotel import gap_fill
from moving_average import mov_avg

'''
Questions for Kelly:
might as well use snotel HS?
'''

file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/FST_1hr_dirty.csv'
caca = pd.read_csv(file_path)

print(caca.columns)
caca['flag'] = 0

caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')

caca['hs_cm'] = mov_avg(caca.index, caca['hs_cm'], weight=False, w_size=50)


'''
diff = caca['hs_cm'].diff().abs()
diff_ix = diff <= 15
caca['hs_cm'] = caca['hs_cm'][diff_ix]
caca.loc[~diff_ix, 'flag'] = 1
'''

snotel = pd.read_csv('ref_stations/FST_2425_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
snotel.rename(columns={'SNWD.I-1 (in) ': 'hs_cm',
                       'WTEQ.I-1 (in) ': 'swe_mm',
                       'TOBS.I-1 (degC) ': 'temp_c'
                       },inplace=True)
snotel['hs_cm'] *= 2.54 # convert hs to cm
sno_ix = snotel['hs_cm'] > 0 # index
snotel['hs_cm'] = snotel['hs_cm'][sno_ix] # filter
snotel['hs_cm'] = mov_avg(snotel.index, snotel['hs_cm'], 30, False)
snotel['swe_mm'] *= 25.4 # convert swe to mm
sno_dt = pd.to_datetime(snotel['Date'] + ' ' + snotel['Time']) # convert to date time
snotel.set_index(sno_dt, inplace=True)

plt.plot(caca['date'], caca['hs_cm'] - 44, label='FST_hs - 44cm')
plt.plot(snotel['hs_cm'], label='snotel')
plt.legend()
plt.tight_layout()
plt.show()
