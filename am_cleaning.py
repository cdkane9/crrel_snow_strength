import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gap_fil_snotel import gap_fill
from moving_average import mov_avg

site_raw = pd.read_csv(
        f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/wx_stations/AM_2024_2025_1hr_raw.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False,
        skiprows=[0, 2, 3])

for i in site_raw.columns:
    print(i)

site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')

site_raw['DBTCDT'] = site_raw['DBTCDT'].astype(float) - 18

diff = site_raw['DBTCDT'].diff().abs()
diff_ix = diff <= 15
site_raw['DBTCDT'] = site_raw['DBTCDT'][diff_ix]
print(site_raw.tail)
plt.plot(site_raw['Albedo_Avg'].astype(float), label='Albedo')
plt.legend()
plt.title('AM')
plt.show()

site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/AlpineMeadow_2024_2025_1hr_raw.dat')
'''
file_path = '/Users/colemankane/Desktop/crrel_exports/wx_stations/AM_1hr_dirty.csv'
caca = pd.read_csv(file_path)
print(caca.columns)
caca['date'] = pd.to_datetime(caca['date'], format='%Y-%m-%d %H:%M:%S')

# write moving window average in different file other than fre_cleaning
#caca['hs_cm'] = mov_avg(caca.index, caca['hs_cm'], 30, False)
caca.set_index('date', inplace=True)


caca['flag'] = 0

caca['hs_cm'] -= 20

diff = caca['hs_cm'].diff().abs()
diff_ix = diff <= 15
caca['hs_cm'] = caca['hs_cm'][diff_ix]
caca.loc[~diff_ix, 'flag'] = 1



plt.plot(caca['temp1_c'], label='temp_1')
plt.plot(caca['temp2_c'], label='temp_2')
plt.legend()
plt.show()
'''