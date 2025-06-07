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

'''Establish relationship between bdg reservoir snotel and bdg site'''
'''Can make somewhat accurate predictions about bdg site to fill data gaps'''
# define timestamps of gap
sgap = pd.Timestamp("2025-03-23 09:15:00")
egap = pd.Timestamp('2025-04-12 13:30:00')

# add in missing dates
full_idx = pd.date_range(
    start=caca.index.min(),
    end=caca.index.max(),
    freq='15min',
)
caca = caca.reindex(full_idx).interpolate(method='index')


# align two datasets on common indices
aligned = caca.join(snotel, how='inner', lsuffix='caca', rsuffix='snotel')
common_index = caca.index.intersection(snotel.index)
caca_aln = caca.loc[common_index]
stl_aln = snotel.loc[common_index]

# subset where both datasets are not nan
mask = np.isfinite(caca_aln['hs_cm']) & np.isfinite(stl_aln['hs'])
caca_aln = caca_aln[mask]
stl_aln = stl_aln[mask]


# determine differnce between site and snotel on either end of gap
start_gap = caca_aln.loc[sgap, 'hs_cm'] - snotel.loc[sgap, 'hs']
end_gap = caca_aln.loc[egap, 'hs_cm'] - snotel.loc[egap, 'hs']
avg_diff = (start_gap + end_gap) / 2


# define model to go from snotel HS to site HS
m,b = np.polyfit(stl_aln['hs'], caca_aln['hs_cm'],1)
rmse = np.sqrt(mean_squared_error(caca_aln['hs_cm'],
                                   stl_aln['hs'] + b))

# fill gap
stl_fill = snotel[(snotel.index >= sgap) & (snotel.index < egap)].copy()
fill = (m * stl_fill['hs'] + start_gap)

caca.loc[sgap:egap, 'hs_cm'] = fill
caca.loc[sgap:egap, 'flag'] = 1

plt.plot(caca['hs_cm'])
plt.plot(snotel['hs'])
plt.plot(caca['flag'] * 10)
plt.show()






