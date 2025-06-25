import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

site_name = 'Brundage'
site_raw = pd.read_csv(f'wx_stations/{site_name}_15Min.dat',
                       on_bad_lines='skip',
                       delimiter=',',
                       low_memory=False,
                       skiprows=[0, 2, 3])
print(site_raw.columns)
if site_name == 'Brundage':
    site_raw_dt = site_raw['TIMESTAMP']
    site_date = pd.to_datetime(site_raw_dt, format='%Y-%m-%d %H:%M:%S')
    site_hs = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100
    site_temp = site_raw['Temp_C_Avg'].astype(float)
    site_ws = site_raw['WS_ms_S_WVT'].astype(float)
    site_wdir = site_raw['WindDir_SD1_WVT'].astype(float)
    site_swe = site_raw['SS_SWE_Avg'].astype(float)
    site_rh = site_raw['RH'].astype(float)
    site_dist = site_raw['SnoDAR_distance_Avg'].astype(float)
    site = {'date': site_date,
            'hs_cm': site_hs,
            'swe_mm': site_swe,
            'temp_c': site_temp,
            'rh': site_rh,
            'wspd_mps': site_ws,
            'wdir': site_wdir,
            'dist': site_dist
            }

elif site_name == 'Freeman':
    site_raw_dt = site_raw['TIMESTAMP']
    site_date = pd.to_datetime(site_raw_dt, format='%Y-%m-%d %H:%M:%S')
    site_hs = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100
    site_temp = site_raw['Temp_C_Avg'].astype(float)
    site_ws = site_raw['WS_ms_S_WVT'].astype(float)
    site_wdir = site_raw['WindDir_SD1_WVT'].astype(float)
    site_dist = site_raw['SnoDAR_distance_Avg'].astype(float)
    site_rh = site_raw['RH'].astype(float)
    site = {'date': site_date,
            'hs_cm': site_hs,
            'temp_c': site_temp,
            'rh': site_rh,
            'wspd_mps': site_ws,
            'wdir': site_wdir,
            'dist': site_dist}

elif site_name == 'Bogus':
    site_raw_dt = site_raw['TIMESTAMP']
    site_date = pd.to_datetime(site_raw_dt, format='%Y-%m-%d %H:%M:%S')
    site_hs = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100
    site_temp = site_raw['AirTC_Avg'].astype(float)
    site_rh = site_raw['RH'].astype(float)
    site = {'date': site_date,
            'hs_cm': site_hs,
            'temp_c': site_temp,
            'rh': site_rh
            }



site = pd.DataFrame(site)
site = site[(site['date'] >= '2024-10-01 00:00:00')]
site = site.set_index('date')

plt.plot(site['hs_cm'] / 100)
plt.plot(site['dist'])
plt.show()

#site.to_csv(f'/Users/colemankane/Desktop/crrel_exports/wx_stations/{site_name}_15min_dirty.csv')



