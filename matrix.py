import numpy as np
import pandas as pd
import os
import sys
'''
need to add something that checks if force is -1
'''
scope_path = '/Volumes/Seagate Backup Plus Drive/SnowScopes/WY25/20250325'
all_scopes = os.listdir(scope_path)



def matrix_scrubber(matrix_path, id):
    '''
    reads in a hardness matrix file and produces .csv for each data type
    :param matrix_path: where to find matrix
    :return: none, exports to .csv's
    '''

    matrix = pd.read_excel(matrix_path,
                           skiprows=3,
                           na_values='None')

    def get_index(type):
        '''
        finds the indices of different strength measurements
        :param type: str, data type, smp, force_ram, snow scope, etc.
        :return: series of indicies
        '''
        ix = matrix['Data Type'] == type
        return matrix[ix]

    ##############################################
    smp = get_index('SMP')
    ##############################################

    fscope = get_index('Force_Scope').dropna(subset=['SN', 'Profile #']).reset_index(drop=True)

    sn = fscope['SN'].astype(int).astype(str).str.zfill(5)
    pn = fscope['Profile #'].astype(int).astype(str)
    scope_id = 'Profile' + pn + '_SN' + sn + '.csv'

    for i in range(len(scope_id)):
        find_profile = next((x for x in all_scopes if x.endswith(scope_id[i])), None)
        profile_path = f'{scope_path}/{find_profile}'
        profile = pd.read_csv(profile_path, skiprows=24)
        fscope.loc[i, 'max_pressure'] = np.max(profile['hardness (kPa)'])
        fscope.loc[i, 'id'] = id

    ##############################################
    ram_path = '/Users/colemankane/Desktop/crrel_exports/'

    fram = get_index('Force_Std_Ram')
    if not fram.empty:
        depth = fram['Depth_m']
        sram = pd.read_csv(ram_path + id + '_ram.csv')
        for d in range(len(depth)):
            sram = sram[sram['l'] < 80]
            max_rr = np.nanmax(sram['rr'])
            fram['max_rr'] = max_rr
            fram['id'] = id
    else:
        pass


    ##############################################
    scope = get_index('SnowScope')


    export_path = '/Users/colemankane/Desktop/crrel_exports'
    #export_path = '/Users/colemankane/Desktop/flakesense'
    #smp.to_csv(f'{export_path}/{id}_smp.csv', index=False)
    #fscope.to_csv(f'{export_path}/{id}_fscope.csv', index=False)
    #fram.to_csv(f'{export_path}/{id}_fram.csv', index=False)
    #scope.to_csv(f'{export_path}/{id}_scope.csv', index=False)



