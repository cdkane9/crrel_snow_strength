import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gap_fil_snotel import gap_fill
from datetime import datetime

site_raw = pd.read_csv(f'wx_stations/Brundage_2024_2025_15min_raw.dat',
                           on_bad_lines='skip',
                           delimiter=',',
                           low_memory=False,
                           skiprows=[0, 2, 3])
site_raw['SnoDAR_snow_depth_Avg'] = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100
for i in site_raw.columns:
    print(i)

site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')


diff = site_raw['SnoDAR_snow_depth_Avg'].diff().abs()
diff_ix = diff <= 12
site_raw['SnoDAR_snow_depth_Avg'] = site_raw['SnoDAR_snow_depth_Avg'][diff_ix]



hs_start = pd.Timestamp('2025-02-28 14:45:00')
hs_end = pd.Timestamp('2025-03-02 14:45:00')
site_raw.loc[hs_start:hs_end, 'SnoDAR_snow_depth_Avg'] += 200

buried_start = pd.Timestamp('2025-02-17 00:00:00')
buried_end = pd.Timestamp('2025-02-18 14:45:00')

site_raw.loc[buried_start:buried_end, 'SnoDAR_snow_depth_Avg'] = np.nan


site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Brundage_2024_2025_15min_raw.dat')
plt.plot(site_raw['SoilVUE_T_5cm_Avg'].astype(float))
plt.show()



'''
# read in dirty wx_station data
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/Brundage_15min_dirty.csv'
caca = pd.read_csv(file_path)

# convert to data frame, set date as index
caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')
caca.set_index('date', inplace=True)

# create column for flagging data
caca['flag'] = 0

plt.plot(caca['hs_cm'])
plt.show()


# use nearby snotel to help fill gaps
# Read in .csv of nearby snotel (if necessary)
snotel = pd.read_csv('ref_stations/BDG_res_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
snotel.rename(columns={'SNWD.I-1 (in) ': 'hs_cm',
                       'WTEQ.I-1 (in) ': 'swe_mm',
                       'TOBS.I-1 (degC) ': 'temp_c'
                       },inplace=True)
snotel['hs_cm'] *= 2.54 # convert hs to cm
plt.plot(snotel['hs_cm'])
plt.show()
sno_ix = snotel['hs_cm'] > 0 # index
snotel['hs_cm'] = snotel['hs_cm'][sno_ix] # filter
snotel['swe_mm'] *= 25.4 # convert swe to mm
sno_dt = pd.to_datetime(snotel['Date'] + ' ' + snotel['Time']) # convert to date time
snotel.set_index(sno_dt, inplace=True)
snotel = snotel.resample('15min').interpolate() # resample to match time step of study plot




# filter out big jumps in data wx station data
diff = caca['hs_cm'].diff().abs()
diff_ix = diff  <= 15
caca['hs_cm'] = caca['hs_cm'][diff_ix]
caca.loc[~diff_ix, 'flag'] = 1


# snodar was raised, fix hs for two days before re-calibrated
hs_start = pd.Timestamp('2025-02-28 14:45:00')
hs_end = pd.Timestamp('2025-03-02 14:45:00')
caca.loc[hs_start:hs_end, 'hs_cm'] += 200
caca.loc[hs_start:hs_end, 'flag'] = 1


# station shut down for few weeks.  gap fill from bdg_reservoir_snotel
st = '2025-03-23 09:15:00'
end = '2025-04-12 13:30:00'

caca = gap_fill(caca, snotel, st, end, 'hs_cm', 'avg_diff', dategap=True)[0]
caca = gap_fill(caca, snotel, st, end, 'swe_mm', 'b', dategap=True)[0]
caca = gap_fill(caca, snotel, st, end, 'temp_c', 'b', dategap=True)[0]

plt.plot(caca['hs_cm'])
plt.plot(snotel['hs_cm'])
plt.show()

# read granite mountain wx station for wind data
gmt = pd.read_csv('ref_stations/granite_mtn.csv', skiprows=10)
gmt['date'] = pd.to_datetime(gmt['date'], errors='coerce', utc=True)
gmt['date'] = gmt['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
gmt['date'] = pd.to_datetime(gmt['date'], format='%Y-%m-%d %H:%M:%S')
gmt.set_index('date', inplace=True)
gmt = gmt.resample('15min').interpolate(method='index')
'''
