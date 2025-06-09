import numpy as np
import pandas as pd


better_cols = [
    't_kg', # tube mass
    'h_kg', #hammer mass
    'n', # number of falls
    'f_cm', # fall height
    'l_cm', # location of point
    'p_cm', # penetration
    'hag_cm', # height above ground
]
def ram_scrubber(ram_path, id):
    '''
    calculates ram number and ram resistance and exports to .csv
    :param id: pit ID, SITE_YYYYMMDD
    :param ram_path: directory
    :return: none, exports to folder
    '''
    print(id)
    ram = pd.read_excel(ram_path,
                        skiprows=7)

    ram.columns = better_cols
    ram = ram.astype(float)


    # height of snow, or deepest location of point
    hs = ram.iloc[-1,4]

    ram.loc[0, 'p_cm'] = ram.loc[0, 'l_cm']

    #calculates penetration from subsequent trials
    for i in range(len(ram) - 1):
        j = i + 1
        ram.loc[j, 'p_cm'] = ram.loc[j, 'l_cm'] - ram.loc[i, 'l_cm']

    # calculates height above ground
    ram['hag_cm'] = hs - ram['l_cm']

    #drop rows where p=0 to avoid /0
    ram = ram[ram['p_cm'] != 0]

    # calculate ram number, t + h + (nfH)/p
    rn = ram['t_kg'] + ram['h_kg'] + ((ram['n'] * ram['f_cm'] * ram['h_kg']) / ram['p_cm'])

    # calculate ram resistance, rn * g
    rr = rn * 9.81

    # add rn and rr series to one data frame, export
    to_concat = [ram, rn, rr]
    export = pd.concat(to_concat, axis=1)

    #rename columns
    export.columns.values[7] = 'rn_kg'
    export.columns.values[8] = 'rr_N'

    #directory to export
    export_path = '/Users/colemankane/Desktop/crrel_exports'
    if ram_path.endswith('_sram.xlsx'):
        export.to_csv(f'{export_path}/{id}_sram.csv', index=False)
    else:
        export.to_csv(f'{export_path}/{id}_pram.csv', index=False)
    return