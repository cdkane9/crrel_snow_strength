import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


smp_dir = '/Users/colemankane/Library/CloudStorage/GoogleDrive-ColemanKane@boisestate.edu/Shared drives/2024-2025 CRREL Snow Strength/Data/Scrubbed pit strength transect data/crrel_exports'
data_files = os.listdir(smp_dir)

smp_files = [i for i in data_files if i.endswith('_smp.csv')]

profs_to_stitch = pd.read_excel('/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/profs_to_sitch.xlsx',
                                dtype={
                                    'SN': str,
                                    'pn_top': str,
                                    'pn_bot': str,
                                    'ol_cm': float,
                                    'start_cm': float
                                })
profs_to_stitch['SN'] = profs_to_stitch['SN'].str.zfill(2)
profs_to_stitch['pn_top'] = profs_to_stitch['pn_top'].str.zfill(4)
profs_to_stitch['pn_bot'] = profs_to_stitch['pn_bot'].str.zfill(4)

first_row = list(profs_to_stitch.loc[5])

top_path = smp_dir + f'/smp_profiles_exports/S{first_row[0]}M{first_row[1]}.PNT_samples.csv'
bot_path = smp_dir + f'/smp_profiles_exports/S{first_row[0]}M{first_row[2]}.PNT_samples.csv'

top = pd.read_csv(top_path, skiprows=1)
bot = pd.read_csv(bot_path, skiprows=1)

start_bot = first_row[-1] * 10
good_bot = bot[bot['distance [mm]'] >= start_bot].copy()

last_top = top['distance [mm]'].iloc[-1] + 0.0001
first_bot = good_bot['distance [mm]'].iloc[0]

dist_diff = last_top - first_bot

print(last_top, first_bot, dist_diff)

if dist_diff > 0:
    good_bot['distance [mm]'] += dist_diff
else:
    good_bot['distance [mm]'] += dist_diff
    print('else')

print(top.tail())
print(good_bot.head())

export = pd.concat([top, good_bot], ignore_index=True)

plt.plot(export['force [N]'], export['distance [mm]'])
plt.gca().invert_yaxis()
plt.show()






