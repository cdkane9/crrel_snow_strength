import numpy as np
import pandas as pd


better_cols = [
    't', # tube mass
    'h', #hammer mass
    'n', # number of falls
    'f', # fall height
    'l', # location of point
    'p', # penetration
    'hag', # height above ground
]
def ram_scrubber(ram_path, id):
    '''
    calculates ram number and ram resistance and exports to .csv
    :param id: pit ID, SITE_YYYYMMDD
    :param ram_path: directory
    :return: none, exports to folder
    '''
    ram = pd.read_excel(ram_path,
                        skiprows=7)

    ram.columns = better_cols
    ram = ram.astype(float)


    # height of snow, or deepest location of point
    hs = ram.iloc[-1,4]

    ram.loc[0, 'p'] = ram.loc[0, 'l']

    #calculates penetration from subsequent trials
    for i in range(len(ram) - 1):
        j = i + 1
        ram.loc[j, 'p'] = ram.loc[j, 'l'] - ram.loc[i, 'l']

    # calculates height above ground
    ram['hag'] = hs - ram['l']

    #drop rows where p=0 to avoid /0
    ram = ram[ram['p'] != 0]

    # calculate ram number, t + h + (nfH)/p
    rn = ram['t'] + ram['h'] + ((ram['n'] * ram['f'] * ram['h']) / ram['p'])

    # calculate ram resistance, rn * g
    rr = rn * 9.81

    # add rn and rr series to one data frame, export
    to_concat = [ram, rn, rr]
    export = pd.concat(to_concat, axis=1)

    #rename columns
    export.columns.values[7] = 'rn'
    export.columns.values[8] = 'rr'

    #directory to export
    export_path = '/Users/colemankane/Desktop/crrel_exports'

    export.to_csv(f'{export_path}/{id}_ram.csv', index=False)

    return