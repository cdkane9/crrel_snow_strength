import pandas as pd
import os



import_folder = '/Users/colemankane/Desktop/flakesense'
import_dir = os.listdir(import_folder)

scopes = [i for i in import_dir if i.endswith('_scope.csv')]
strats = [i for i in import_dir if i.endswith('_strat.csv')]
export_sheet = []

for i in scopes:
    print(i)
    matrix = pd.read_csv(f'{import_folder}/{i}')
    pit = '_'.join(i.split('_')[:2]) + '_strat.csv'
    export_row = [pit]
    for j in matrix.index:
        sn = str(round(matrix.iloc[j, 4]))
        pn = str(round(matrix.iloc[j, 5]))
        profile = f'Profile{pn}_SN{sn.zfill(5)}.csv'
        export_row.append(profile)
    export_sheet.append(export_row)

export_path = '/Users/colemankane/Desktop/flakesense'
export_cols = ['pit_path', 'scope1', 'scope2', 'scope3', 'scope4', 'scope5']
export_df = pd.DataFrame(export_sheet, columns=None)
export_df.to_csv(f'{export_path}/scope_pit_list.csv', index=False)



