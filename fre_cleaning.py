import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



site_raw = pd.read_csv(f'wx_stations/Freeman_2024_2025_15min_raw.dat',
                           on_bad_lines='skip',
                           delimiter=',',
                           low_memory=False,
                           skiprows=[0, 2, 3])

for i in site_raw.columns:
    print(i)

site_raw['SnoDAR_snow_depth_Avg'] = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100

site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

diff = site_raw['SnoDAR_snow_depth_Avg'].diff().abs()
diff_ix = diff <= 15
site_raw['SnoDAR_snow_depth_Avg'] = site_raw['SnoDAR_snow_depth_Avg'][diff_ix]


site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')

snow_first = pd.Timestamp('2024-10-29 00:00:00')
site_raw.loc[:snow_first, 'SnoDAR_snow_depth_Avg'] = 0

#for i in range(len(site_raw)):
 #   print(site_raw.iloc[i]['DTC_Avg(30)'], site_raw.index[i])

site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Freeman_2024_2025_15min_raw.dat')


plt.plot(site_raw['IR01Up_Avg'].astype(float))
plt.plot(site_raw['SR01Up_Avg'].astype(float))
plt.tight_layout()
plt.show()

'''
# read in dirty wx_station data
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/Freeman_15min_dirty.csv'
caca = pd.read_csv(file_path)

#caca['hs_cm'] = mov_avg(caca.index, caca['hs_cm'], 80, False)


# convert to data frame, set date as index
caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')
caca.set_index('date', inplace=True)

plt.plot(caca['hs_cm'])
plt.show()

# create column for flagging data
caca['flag'] = 0

# use nearby snotel to help fill gaps
# Read in .csv of nearby snotel (if necessary)
snotel = pd.read_csv('ref_stations/MCS_2425_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
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
snotel = snotel.resample('15min').interpolate() # resample to match time step of study plot

s1 = '2025-01-09 22:00:00'
e1 = '2025-01-22 05:30:00'

s2 = '2025-10-26 15:30:00'
e2 = '2025-10-30 12:30:00'

caca, hs_m, hs_b, hs_rmse = gap_fill(caca,
                                  snotel,
                                  s1, e1,
                                  'hs_cm',
                                  'b',
                                  True
                                 )


caca, t_m, t_b, t_rmse = gap_fill(caca, snotel,
                                  s1, e1,
                                  'temp_c',
                                  'b',
                                  True)


caca = gap_fill(caca, snotel,
                s2, e2,
                'temp_c',
                'b', True, False)[0]



caca = gap_fill(caca, snotel,
                s2, e2,
                'temp_c',
                'b', True)[0]

no_snow = caca.index <= '2024-10-07 00:00:00'
caca.loc[no_snow, 'hs_cm'] = 0


plt.plot(caca['hs_cm'])
plt.plot(snotel['hs_cm'])
plt.show()

pilot = pd.read_csv('pilot_station.csv', skiprows=10)
pilot['wspd_mps'] = pilot['wspd_mps'].astype(float)
pilot['date'] = pd.to_datetime(pilot['date'], errors='coerce', utc=True)
pilot['date'] = pilot['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
pilot['date'] = pd.to_datetime(pilot['date'], format='%Y-%m-%d %H:%M:%S')
pilot.set_index('date', inplace=True)
pilot.index = pilot.index - pd.Timedelta(minutes=6)

#caca, w_m, w_b, w_rmse = gap_fill(caca, pilot,
#                                  s1, e1,
#                                  'wspd_mps',
#                                  'b',
#                                  True, False)

caca.to_csv('/Users/colemankane/Desktop/crrel_exports/wx_stations/Freeman_15min_cleaned_gapfilled.csv')
'''