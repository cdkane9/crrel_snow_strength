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
results = []

for f in range(len(frams)):
    fram = pd.read_csv(data_dir + '/' + frams[f])
    if not fram.empty:
        max_force = list(fram['Max Force'])
        max_rr = list(fram['max_rr'])
        id = list(fram['id'])
        for i in range(len(max_force)):
            results.append([max_rr[i], max_force[i], id[i]])



comp = pd.DataFrame(results, columns=['rr', 'force', 'id'])
comp = comp[comp['rr'] <= 400]
comp['rr'] = comp['rr'].astype(float)
comp['force'] = comp['force'].astype(float)


grouped = comp.groupby('id')[['rr', 'force']]
means = grouped.mean()
stds = grouped.std()

avg_rr = np.array(means['rr']).reshape(-1,1)
avg_force = np.array(means['force'])

def rmse(actual, predicted):
    error = actual - predicted
    mean = np.nanmean(error ** 2)
    root = np.sqrt(mean)
    return root

model = LinearRegression(fit_intercept=False)
model.fit(avg_rr, avg_force)
m = model.coef_[0]
root_error = rmse(means['force'], means['rr'] * m)


r2 = (sklearn.metrics.r2_score(means['force'], means['rr'] * m))



x = np.linspace(0, 400, len(means['rr']))
plt.scatter(means['rr'], means['force'], color='black')
plt.errorbar(means['rr'], means['force'],
             xerr=stds['rr'], yerr=stds['force'],
             fmt='o', capsize=3, elinewidth=2, markeredgewidth=0.5, color='black')
plt.plot(x, x * m, color='darkslategray',
         label = f'y = {round(m, 2)}x \n'
         f'RMSE = {round(root_error, 2)} \n'
         f'R2 = {round(r2, 2)}')
plt.xlabel('Ram Resistance (N)', fontsize=20)
plt.ylabel('Force (N)', fontsize=20)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()

'''
model.fit(max_rr.reshape(-1, 1), max_force)

m = model.coef_[0]

root_error = rmse(max_force, max_rr * m)
r2 = (sklearn.metrics.r2_score(max_force, max_rr * m))

x = np.linspace(0, 1300, len(max_rr))
plt.xlabel('Max RR (N)', fontsize=20)
plt.ylabel('Max Force (N)', fontsize=20)
plt.scatter(max_rr, max_force, color = 'black')
plt.plot(x, m * x, color='darkslategrey', label=f'y = {round(m, 2)}x \n'
                                                f'RMSE = {round(root_error, 2)} \n'
                                                f'R2 = {round(r2, 2)}')
#plt.plot(x, 1 * x, linestyle=':')
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()
'''









