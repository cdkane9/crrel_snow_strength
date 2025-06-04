import pandas as pd
import numpy as np
from matplotlib import pyplot as plt



snotel_raw = pd.read_csv('BDG_res_snotel.csv',
                         delimiter=',',
                         low_memory=False,
                         skiprows=6)

stl_hs = snotel_raw['SNWD.I-1 (in) '] * 0.254 #convert snotel to m
stl_hs_ix = stl_hs > 0
stl_hs = stl_hs[stl_hs_ix]




site_raw = pd.read_csv('Brundage_15Min.dat',
                       delimiter=',',
                       low_memory=False,
                       skiprows=[0, 2, 3])
site_raw_dt = site_raw['TIMESTAMP']
site_date = pd.to_datetime(site_raw_dt, format='%Y-%m-%d %H:%M:%S')
site_hs = site_raw['SnoDAR_snow_depth_Avg'].astype(float) * 100
site_temp = site_raw['Temp_C_Avg'].astype(float)
site_ws = site_raw['WS_ms_S_WVT'].astype(float)
site_wdir = site_raw['WindDir_SD1_WVT'].astype(float)
site_swe = site_raw['SS_SWE_Avg'].astype(float)

site = {'date': site_date,
        'hs_cm': site_hs,
        'swe_mm': site_swe,
        'temp_c': site_temp,
        'wspd_mps': site_ws,
        'wdir': site_wdir,
        }

site = pd.DataFrame(site)



