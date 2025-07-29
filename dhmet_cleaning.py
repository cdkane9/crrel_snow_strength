import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
'''
Hs sensor super noisy, removed spikes
Tair_2_Avg inversed?
No values for Tskin
'''


site_raw = pd.read_csv(
        f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/wx_stations/DHMet_2425_1hr.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False,
        skiprows=[0, 2, 3])

for i in site_raw.columns:
    print(i)

site_raw['TIMESTAMP'] = pd.to_datetime(site_raw["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

site_raw = site_raw[(site_raw['TIMESTAMP'] >= '2024-10-01 00:00:00')]
site_raw = site_raw.set_index('TIMESTAMP')

site_raw['DBTCDT'] = site_raw['DBTCDT'].astype(float) - 115

peak_start = pd.Timestamp('2025-02-18 00:00:00')
peak_end = pd.Timestamp('2025-02-22 00:00:00')

mask1 = (site_raw.index <= peak_start) & (site_raw['DBTCDT'] > 130)
site_raw.loc[mask1, 'DBTCDT'] = np.nan

mask2 = (site_raw.index >= peak_end) & (site_raw['DBTCDT'] > 130)
site_raw.loc[mask2, 'DBTCDT'] = np.nan

site_raw.loc[pd.Timestamp('2024-12-27 02:40:00'), 'DBTCDT'] = np.nan

g_temp_start = pd.Timestamp('2024-12-21 17:00:00')
g_temp_mask = (site_raw.index < g_temp_start)

site_raw.loc[g_temp_mask, 'Tgrd_1_C_Avg'] = np.nan
site_raw.loc[g_temp_mask, 'Tgrd_2_C_Avg'] = np.nan
site_raw.loc[g_temp_mask, 'Tgrd_3_C_Avg'] = np.nan



plt.plot(site_raw['RH_1'].astype(float))
#plt.plot(site_raw['WindDir_2_SD1_WVT'].astype(float))
plt.show()

site_raw.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/DeadHorseMet_2024_2025_1hr_raw.dat')