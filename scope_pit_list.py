import pandas as pd
import os

export_folder = "/Users/colemankane/Desktop/crrel_exports"

export_dir = os.listdir(export_folder)

scopes = [i for i in export_dir if i.endswith("_scope.csv")]

export_sheet = []

for i in scopes:
    matrix = pd.read_csv(f'{export_folder}/{i}')
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
export_df = pd.DataFrame(export_sheet, columns=export_cols)
export_df.to_csv(f'{export_path}/scope_pit_list.csv', index=False)
print(export_df)


