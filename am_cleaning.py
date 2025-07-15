import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gap_fil_snotel import gap_fill
from fre_cleaning import mov_avg

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



plt.plot(caca['wspd_mps'])
plt.show()
