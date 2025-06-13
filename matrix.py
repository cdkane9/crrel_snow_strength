import numpy as np
import pandas as pd
import os
import snowmicropyn as smp
import sys
'''
need to add something that checks if force is -1
'''
export_path = '/Users/colemankane/Desktop/crrel_exports'
scope_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data/Snow_Scope/'
all_scopes = os.listdir(scope_path)
scope_list = []

smp_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data/SMP/'

def matrix_scrubber(matrix_path, id):
    '''
    reads in a hardness matrix file and produces .csv for each data type
    :param matrix_path: where to find matrix
    :return: none, exports to .csv's
    '''
    #print(f'Scrubbing {matrix_path}, {id}...')
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
    #if 'Force_dummy' in matrix['Data Type'].values:
    #    print(matrix_path)
    #if 'force_dummy' in matrix['Data Type'].values:
    #    print(matrix_path)
    #if 'Force_scope' in matrix['Data Type'].values:
    #    print(matrix_path)
    ##############################################
    smp_ix = get_index('SMP')
    if not smp_ix.empty:

        smp_ix.to_csv(f'{export_path}/{id}_smp.csv', index=False)
        smp_sn = smp_ix['SN'].astype(int).astype(str).str.zfill(2)
        smp_pn = smp_ix['Profile #'].astype(int).astype(str).str.zfill(4)
        smp_profile = 'S' + smp_sn + 'M' + smp_pn + '.PNT'
        smp_profile = list(smp_profile)

        #print(smp_profile)
        for i in range(len(smp_profile)):
            p = smp.Profile.load(smp_path + smp_profile[i])
            grd = p.detect_ground()
            surf = p.detect_ground()
            #p.export_derivatives(f'/Users/colemankane/Desktop/crrel_exports/smp_profiles/{smp_profile[i]}_derivatives.csv',
            #                     precision=4, snowpack_only=True)
            #p.export_samples(f'/Users/colemankane/Desktop/crrel_exports/smp_profiles/{smp_profile[i]}_samples.csv',
            #                 precision=4, snowpack_only=True)
        else:
            pass


    ##############################################
    fscope = get_index('Force_Scope').reset_index(drop=True)

    if not fscope.index.empty:
        fscope.to_csv(f'{export_path}/{id}_fscope.csv', index=False)
        try:
            fscope_sn = fscope['SN'].astype(int).astype(str).str.zfill(5)
            fscope_pn = fscope['Profile #'].astype(int).astype(str)
            scope_list.append('Profile' + fscope_pn + '_SN' + fscope_sn)
        except Exception as e:
            print(f'failed at {id}: {e}')
    else:
        pass


    ##############################################

    ram_path = '/Users/colemankane/Desktop/crrel_exports/'

    fram = get_index('Force_Std_Ram')
    if not fram.empty:
        fram.to_csv(f'{export_path}/{id}_fram.csv', index=False)
    else:
        pass


    ##############################################
    scope = get_index('SnowScope')

    if not scope.index.empty:
        try:
            scope.to_csv(f'{export_path}/{id}_scope.csv', index=False)
            scope_sn = scope['SN'].astype(int).astype(str).str.zfill(5)
            scope_pn = scope['Profile #'].astype(int).astype(str)
            scope_list.append('Profile' + scope_pn + '_SN' + scope_sn)
        except Exception as e:
            print(f'error reading {matrix_path}: {e}')

    ##############################################



    #scope.to_csv(f'{export_path}/{id}_scope.csv', index=False)



