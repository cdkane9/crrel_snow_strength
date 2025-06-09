import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from gap_fil_snotel import gap_fill
from datetime import datetime

def mov_avg(x, y, w_size, weight=False):
    '''
    calculates moving window average of a dataset
    :param x: independent variable of a dataset
    :param y: dependent variable of a dataset
    :param w_size: window size
    :param weight: default false. whether to calculate weighted moving window average
    :return: moving average of y-values
    '''
    mov_mean = np.zeros(len(x))  # initiate array
    if not weight:
        count = 0
        for i in x:
            xlow = i - w_size / 2
            xhigh = i + w_size / 2
            Ix = np.logical_and(x > xlow, x < xhigh)
            wind_avg = np.mean(y[Ix])
            mov_mean[count] = wind_avg
            count +=1
    else:
        count = 0
        for i in x:
            xlow = i - w_size / 2
            xhigh = i + w_size / 2
            Ix = np.logical_and(x > xlow, x < xhigh)
            y_mod = y[Ix]
            weights = []
            for j in x[Ix]:
                weight = (15 / 16) * (1 - ((j - i) / (w_size / 2)) ** 2) ** 2
                weights.append(weight)
            ymod_denom = sum(weights)
            ymod_num = y_mod * weights
            ymod = sum(ymod_num) / ymod_denom
            mov_mean[count] = ymod
            count += 1
    return mov_mean

# read in dirty wx_station data
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/Freeman_15min_dirty.csv'
caca = pd.read_csv(file_path)

caca['hs_cm'] = mov_avg(caca.index, caca['hs_cm'], 80, False)

# convert to data frame, set date as index
caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')
caca.set_index('date', inplace=True)


# create column for flagging data
caca['flag'] = 0
plt.plot(caca['hs_cm'])
# use nearby snotel to help fill gaps
# Read in .csv of nearby snotel (if necessary)
snotel = pd.read_csv('ref_stations/MCS_snotel.csv', delimiter=',', low_memory=False, skiprows=6)
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
plt.subplot(2,1,1)
plt.plot(caca['hs_cm'])
plt.subplot(2,2,2)
plt.plot(caca['temp_c'])
plt.show()

caca, t_m, t_b, t_rmse = gap_fill(caca, snotel,
                                  s1, e1,
                                  'temp_c',
                                  'b',
                                  True)
plt.subplot(2,1,1)
plt.plot(caca['hs_cm'])
plt.subplot(2,1,2)
plt.plot(caca['temp_c'])
plt.show()

caca = gap_fill(caca, snotel,
                s2, e2,
                'temp_c',
                'b', True, False)[0]

plt.subplot(2,1,1)
plt.plot(caca['hs_cm'])
plt.subplot(2,1,2)
plt.plot(caca['temp_c'])
plt.show()

caca = gap_fill(caca, snotel,
                s2, e2,
                'temp_c',
                'b', True)[0]

plt.subplot(2,1,2)
plt.plot(caca['hs_cm'])
plt.subplot(2,1,1)
plt.plot(caca['temp_c'])
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
