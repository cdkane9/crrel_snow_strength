import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bog = pd.read_csv(
        f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Bogus_2024_2025_15min_raw.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False)
print(bog.columns)
bog['TIMESTAMP'] = pd.to_datetime(bog["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

bdg = pd.read_csv(
        f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Brundage_2024_2025_15min_raw.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False)
bdg['TIMESTAMP'] = pd.to_datetime(bdg["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')



fre = pd.read_csv(
        f'/Users/colemankane/Desktop/crrel_exports/wx_stations/Freeman_2024_2025_15min_raw.dat',
        on_bad_lines='skip',
        delimiter=',',
        low_memory=False)
fre['TIMESTAMP'] = pd.to_datetime(fre["TIMESTAMP"], format='%Y-%m-%d %H:%M:%S')

plt.plot(bog['TIMESTAMP'], bog['SnoDAR_snow_depth_Avg'].astype(float) * 100, label='Bogus')
plt.plot(bdg['TIMESTAMP'], bdg['SnoDAR_snow_depth_Avg'].astype(float), label='Brundage')
plt.plot(fre['TIMESTAMP'], fre['SnoDAR_snow_depth_Avg'].astype(float), label='Freeman')
plt.legend(loc='upper left')
plt.xlabel('Date')
plt.ylabel('HS (cm)')
plt.title('Snow depth at study plots in Idaho')
plt.tight_layout()
plt.show()
