import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

site_raw = pd.read_csv(
        f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/wx_stations/FST_2425_1hr.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False,
        skiprows=[0, 2, 3])

for i in site_raw.columns:
    print(i)


site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')

too_big = site_raw['DBTCDT'] < 250
site_raw['DBTCDT'] = site_raw['DBTCDT'][too_big]

site_raw['DBTCDT'] = site_raw['DBTCDT'].astype(float) - 29

diff = site_raw['DBTCDT'].diff().abs()
diff_ix = diff <= 10
site_raw['DBTCDT'] = site_raw['DBTCDT'][diff_ix]

s_mess = pd.Timestamp('2024-11-01 00:00:00')
e_mess = pd.Timestamp('2025-02-11 00:00:00')

mask = (site_raw.index >= s_mess) & (site_raw.index <= e_mess) & (site_raw['DBTCDT'] > 145)
site_raw.loc[mask, 'DBTCDT'] = np.nan

early_s = pd.Timestamp('2024-10-01 00:00:00')
early_e = pd.Timestamp('2024-11-17 00:00:00')
mask2 = (site_raw.index >= early_s) & (site_raw.index <= early_e) & (site_raw['DBTCDT'] > 80)
site_raw.loc[mask2, 'DBTCDT'] = np.nan

end = pd.Timestamp('2025-06-09 12:00:00')
mask3 = (site_raw.index >= end) & (site_raw['DBTCDT'] > 80)
site_raw.loc[mask3, 'DBTCDT'] = np.nan


plt.plot(site_raw['Tair_1_Avg'].astype(float))
plt.title('FST')
plt.show()

site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/FoolSnotel_2024_2025_1hr_raw.dat')


'''
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/FoolSnotel_.csv'
caca = pd.read_csv(file_path)

print(caca.columns)
caca['flag'] = 0

caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')

#



#diff = caca['hs_cm'].diff().abs()
diff_ix = caca['hs_cm'] <= 245
caca['hs_cm'] = caca['hs_cm'][diff_ix]
caca.loc[~diff_ix, 'flag'] = 1

#caca['hs_cm'] = mov_avg(caca.index, caca['hs_cm'], weight=False, w_size=24)


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

plt.plot(caca['date'], caca['hs_cm'] - 115, label='FST_hs')
plt.plot(snotel['hs_cm'], label='snotel')
plt.legend()
plt.tight_layout()
plt.show()
'''