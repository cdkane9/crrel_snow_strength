import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# read in dirty wx_station data
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/Brundage_15min_dirty.csv'
caca = pd.read_csv(file_path)

# convert to data frame, set date as index
caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')
caca.set_index('date', inplace=True)

# create column for flagging data
caca['flag'] = 0


# use nearby snotel to help fill gaps
# Read in .csv of nearby snotel (if necessary)
snotel = pd.read_csv('BDG_res_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
snotel.rename(columns={'SNWD.I-1 (in) ': 'hs',
                       'WTEQ.I-1 (in) ': 'swe',
                       'TOBS.I-1 (degC) ': 'temp'
                       },inplace=True)
snotel['hs'] *= 2.54 # convert hs to cm
sno_ix = snotel['hs'] > 0 # index
snotel['hs'] = snotel['hs'][sno_ix] # filter
snotel['swe'] *= 25.4 # convert swe to mm
sno_dt = pd.to_datetime(snotel['Date'] + ' ' + snotel['Time']) # convert to date time
snotel.set_index(sno_dt, inplace=True)

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

'''Establish relationship between bdg reservoir snotel and bdg site'''
'''Can make somewhat accurate predictions about bdg site to fill data gaps'''

# resample wx station to hourly timesteps
caca_hr = caca.resample('h').mean()


# align two datasets on common indices
aligned = caca_hr.join(snotel, how='inner', lsuffix='_df1', rsuffix='_df2')
common_index = caca_hr.index.intersection(snotel.index)
hr_aln = caca_hr.loc[common_index]
stl_aln = snotel.loc[common_index]

# subset where both datasets are not nan
mask = np.isfinite(hr_aln['hs_cm']) & np.isfinite(stl_aln['hs'])
hr_aln = hr_aln[mask]
stl_aln = stl_aln[mask]

#determine how closely related two sites are
m, b = np.polyfit(stl_aln['hs'], hr_aln['hs_cm'], 1) # use m as coefficient for scaling up snotel data
rmse = np.sqrt(mean_squared_error(hr_aln['hs_cm'], m * stl_aln['hs'] + b))


# fill two week gap end of march
sgap = pd.Timestamp("2025-03-23 09:00:00")
egap = pd.Timestamp('2025-04-12 17:00:00')

# determine difference between site and snotel on either end of the gap
start_gap = caca_hr.loc[sgap, 'hs_cm'] - snotel.loc[sgap, 'hs']
end_gap = caca_hr.loc[egap, 'hs_cm'] - snotel.loc[egap, 'hs']
avg_diff = (start_gap + end_gap) / 2

# fill gap
stl_fill = snotel[(snotel.index >= sgap) & (snotel.index < egap)].copy()
fill = (m * stl_fill['hs'] + avg_diff).resample('15min').interpolate()

caca_hr.loc[sgap:egap, 'hs_cm'] = fill
caca_hr.loc[sgap:egap, 'flag'] = 1

plt.plot(caca_hr['hs_cm'])
plt.plot(caca_hr['flag'])
plt.show()
'''
snotel.to_csv('/Users/colemankane/Desktop/bg_snotel.csv')
caca_hr.to_csv('/Users/colemankane/Desktop/bg_caca.csv')'''




