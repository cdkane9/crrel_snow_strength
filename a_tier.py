import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

data_dir = '/Users/colemankane/Desktop/crrel_exports'
data_lst = os.listdir(data_dir)

#comp = pd.DataFrame(columns=['max_force', 'max_rr'])

frams = [i for i in data_lst if i.endswith('fram.csv')]
comp = np.zeros((len(frams), 2))

for f in range(len(frams)):
    fram = pd.read_csv(data_dir + '/' + frams[f])
    if not fram.empty:
        max_force = np.nanmean(fram['Max Force'])
        max_rr = np.nanmean(fram['max_rr'])
        #comp = pd.concat([comp, pd.DataFrame({'max_force': max_force, 'max_rr': max_rr})])
        comp[f, 0] = max_force
        comp[f, 1] = max_rr
    else:
        pass

max_force = comp[:, 0]
max_rr = comp[:, 1]

