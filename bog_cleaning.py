import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
site_raw = pd.read_csv(f'wx_stations/Bogus_2024_2025_15min_raw.dat',
                           on_bad_lines='skip',
                           delimiter=',',
                           low_memory=False,
                           skiprows=[0, 2, 3])

for i in site_raw.columns:
    print(i)

site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

site_raw['SnoDAR_snow_depth_2'] = site_raw['SnoDAR_snow_depth_2'].astype(float) * 100

site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')

plt.plot(site_raw['DTC_Avg(15)'].astype(float))
plt.show()

site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_2024_2025_15min_raw.dat')

'''
site = pd.read_csv('/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_15min_dirty.csv')
site['date'] = pd.to_datetime(site['date'], format='%Y-%m-%d %H:%M:%S')
site.set_index('date', inplace=True)
site['flag'] = 0



stl = pd.read_csv('/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/ref_stations/BOG_2425_snotel.csv',
                  delimiter=',', low_memory=False, skiprows=6)
stl.rename(columns={'SNWD.I-1 (in) ': 'hs_cm',
                       'WTEQ.I-1 (in) ': 'swe_mm',
                       'TOBS.I-1 (degC) ': 'temp_c'
                       },inplace=True)


stl['hs_cm'] *= 2.54 # convert hs to cm
sno_ix = stl['hs_cm'] > 0 # index
stl['hs_cm'] = stl['hs_cm'][sno_ix] # filter
stl['swe_mm'] *= 25.4 # convert swe to mm
sno_dt = pd.to_datetime(stl['Date'] + ' ' + stl['Time']) # convert to date time
stl.set_index(sno_dt, inplace=True)
stl = stl.resample('15min').interpolate()

print(np.max(stl['hs_cm']))

hs_s = '2024-12-15 04:15:00'
hs_e = '2025-01-10 14:45:00'

t1_s = '2025-04-19 00:00:00'
t1_e = '2025-05-09 02:45:00'

t2_s = '2025-05-19 10:00:00'
t2_e = '2025-06-01 20:00:00'


site = gap_fill(
    site,
    stl,
    t1_s, t1_e, 'temp_c', 'b')[0]

site = gap_fill(
    site,
    stl,
    t2_s, t2_e,
    'temp_c', 'b'
)[0]

site = gap_fill(
    site,
    stl,
    hs_s, hs_e,
    'hs_cm', 'avg_diff', dategap=True

)[0]

plt.plot(site['hs_cm'])
plt.show()
site.to_csv('/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_15min_cleaned_gapfilled.csv')

'''
