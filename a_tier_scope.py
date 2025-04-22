import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import sklearn
from sklearn.linear_model import LinearRegression


data_dir = '/Users/colemankane/Desktop/crrel_exports'
data_lst = os.listdir(data_dir)


fscopes = [i for i in data_lst if i.endswith('_fscope.csv')]
results = []

for f in range(len(fscopes)):
    fscope = pd.read_csv(data_dir + '/' + fscopes[f])
    if not fscope.empty:
        max_force = list(fscope['Max Force'])
        max_pressure = list(fscope['max_pressure'])
        id = list(fscope['id'])
        for i in range(len(max_force)):
            results.append([max_force[i], max_pressure[i], id[i]])


comp = np.array(results)
f_out_ix = comp[:, 0].astype(float) < 100


comp_out = comp[f_out_ix]
max_f = comp_out[:, 0].astype(float)
max_kpa = comp_out[:, 1].astype(float)



def rmse(actual, predicted):
    error = actual - predicted
    mean = np.nanmean(error ** 2)
    root = np.sqrt(mean)
    return root

model = LinearRegression(fit_intercept=False)
model.fit(max_kpa.reshape(-1, 1), max_f)

m = model.coef_[0]
root_error = rmse(max_f, max_kpa * m)
print(m)
r2 = (sklearn.metrics.r2_score(max_f, max_kpa * m))
print(root_error)
print(r2)
"""
x = np.linspace(0, 600, len(max_kpa))
plt.scatter(max_kpa, max_f, color = 'black')
plt.xlabel('Max Pressure (kPa)', fontsize=20)
plt.ylabel('Max Force (N)', fontsize=20)
plt.plot(x, m * x, color = 'darkslategrey',
         label = f'y = {round(m,2)}x \n'
                 f'RMSE = {round(root_error,2)} \n'
                 f'R2 = {round(r2,2)}')
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()

"""





#plt.scatter(max_f, max_kpa)
#plt.show()




