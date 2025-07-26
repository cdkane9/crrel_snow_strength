import numpy as np
import pandas as pd
import re
def transect_scrubber(trans_path, id):
    print(trans_path, id)
    site = id.split('_')[0]
    match = re.search(r'HStransect([A-Za-z0-9]+)\.xlsx$', trans_path)
    if match:
        if match.group(1) == 'JPLA':
            end = 'SNA'
        else:
            end = match.group(1)
    trans = pd.read_excel(trans_path,
                          usecols='B:M',
                          skiprows=0)

    if trans_path.endswith('JPLA.xlsx'):
        caca = trans.iloc[8:, 0:4]
        caca.columns = ['pt', 'label', 'dist_m', 'hs_cm']


    else:
        # isolate depth measurements
        caca = trans.iloc[8:, 0:2].reset_index(drop=True)
        caca.columns = ['pt', 'hs_cm']
        first_na = caca['hs_cm'].isna().idxmax()
        caca = caca.loc[:first_na - 1]

    # pull out header date
    date = trans.iloc[1, 8]
    time_start = trans.iloc[2, 10]
    time_end = trans.iloc[2, 11]

    caca['avg_hs_cm'] = None
    caca['std_hs_cm'] = None
    caca['date'] = None
    caca['t_start'] = None
    caca['t_end'] = None

    caca.at[0, 'date'] = date
    caca.at[0, 't_start'] = time_start
    caca.at[0, 't_end'] = time_end
    caca.at[0, 'avg_hs_cm'] = round(np.nanmean(caca['hs_cm']),1)
    caca.at[0, 'std_hs_cm'] = round(np.nanstd(caca['hs_cm']), 1)

    if trans_path.split('_')[-3] == 'TS':
        id = f'{site}_{date}_TS_{time_start}'
        print('TIME SERIES')
    export_path = f'/Users/colemankane/Desktop/20250715_den_hs_for_stine/{id}_transect{end}.csv'
    caca.to_csv(export_path, index=False)




