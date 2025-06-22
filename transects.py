import pandas as pd

def transect_scrubber(trans_path, id):
    trans = pd.read_excel(trans_path,
                          usecols='B:M',
                          skiprows=0)

    # isolate depth measurements
    caca = trans.iloc[8:, 0:2].reset_index(drop=True)
    caca.columns = ['pt', 'hs_cm']
    first_na = caca['hs_cm'].isna().idxmax()
    caca = caca.loc[:first_na - 1]

    # pull out header date
    date = trans.iloc[1, 8]
    time_start = trans.iloc[2, 10]
    time_end = trans.iloc[2, 11]

    caca['date'] = None
    caca['t_start'] = None
    caca['t_end'] = None

    caca.at[0, 'date'] = date
    caca.at[0, 't_start'] = time_start
    caca.at[0, 't_end'] = time_end

    if trans_path.split('_')[-3] == 'TS':
        id = f'{site}_{date}_TS_{time_start}'
        print('TIME SERIES')
    export_path = f'/Users/colemankane/Desktop/crrel_exports/{id}_transect.csv'
    #caca.to_csv(export_path, index=False)


path_in = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data/Colorado/Sites/AM/20250108/AM_20250108_HStransectA.xlsx'
id = 'AM_20250108'
transect_scrubber(path_in, id)


