import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import sklearn
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

data_dir = '/Users/colemankane/Desktop/crrel_exports'
data_lst = os.listdir(data_dir)

#comp = pd.DataFrame(columns=['max_force', 'max_rr'])

frams = [i for i in data_lst if i.endswith('fram.csv')]
rcomp = np.zeros((len(frams), 2))

for f in range(len(frams)):
    fram = pd.read_csv(data_dir + '/' + frams[f])
    if not fram.empty:
        max_force = np.nanmean(fram['Max Force'])
        max_rr = np.nanmean(fram['max_rr'])
        #comp = pd.concat([comp, pd.DataFrame({'max_force': max_force, 'max_rr': max_rr})])
        rcomp[f, 0] = max_force
        rcomp[f, 1] = max_rr
    else:
        pass
force = rcomp[:, 0].reshape(-1, 1)
rr = rcomp[:, 1]
f_out_ix = rr < 400

force_out = force[f_out_ix]
rr_out = rr[f_out_ix]

def rmse(actual, predicted):
    error = actual - predicted
    mean = np.nanmean(error ** 2)
    root = np.sqrt(mean)
    return root

model = LinearRegression(fit_intercept=False)

model.fit(force_out, rr_out)

m = model.coef_[0]

root_error = rmse(rr_out, force_out * m)
r2 = (sklearn.metrics.r2_score(rr_out, force_out * m))

x = np.linspace(0, 200, len(rr))
plt.xlabel('Max Force (N)', fontsize=20)
plt.ylabel('Max RR (N)', fontsize=20)
plt.scatter(force_out, rr_out, color = 'black')
plt.plot(x, m * x, color='darkslategrey', label=f'y = {round(m, 2)}x, \n'
                                                f'RMSE = {round(root_error, 2)}, \n'
                                                f'R2 = {round(r2, 2)}')
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()










