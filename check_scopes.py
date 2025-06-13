import pandas as pd
import os

master_path = '/Users/colemankane/Desktop/crrel_exports/scope_master_list.csv'
scope_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data/Snow_Scope'

master = pd.read_csv(master_path, skiprows=0)
master.columns = ['id']
print(master.columns)
scopes = os.listdir(scope_path)

scope_end = [f.replace('.csv', '').split('_')[-2] + '_' + f.replace('.csv', '').split('_')[-1] for f in scopes]
print(scope_end)
master['Exists'] = master['id'].isin(scope_end)

print(len(master[master['Exists'] == False]))