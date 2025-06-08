import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from gap_fil_snotel import gap_fill

site = pd.read_csv('/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_15min_dirty.csv')
site['date'] = pd.to_datetime(site['date'], format='%Y-%m-%d %H:%M:%S')
site.set_index('date', inplace=True)
site['flag'] = 0

stl = pd.read_csv('/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/BOG_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
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


site.to_csv('/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_15min_cleaned_gapfilled.csv')


