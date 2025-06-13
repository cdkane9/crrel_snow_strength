import pandas as pd
#import numpy as np
import os
#from pits import pit_scrubber
#from ram import ram_scrubber
from matrix import matrix_scrubber, scope_list


state = ['Wyoming', 'Colorado', 'Colorado_2', 'Colorado_3', 'Idaho']
data_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data'

matrix_lst = []
pit_lst = []
sram_lst = []
pram_lst = []
ssa_lst = []

# following for loops iterate through state->site->date->data and pulls out data sheets
# appends the file path to corresponding list

for state in state:
    state_path = data_path + f'/{state}/Sites'
    state_dir = [i for i in os.listdir(state_path) if i != '.DS_Store']


    for site in state_dir:
        site_path = state_path + f'/{site}'
        site_dir = [i for i in os.listdir(site_path) if i != '.DS_Store']


        for date in site_dir:
            file_path = site_path + f'/{date}'
            date_dir = [i for i in os.listdir(file_path) if i != '.DS_Store']


            matrix = next((i for i in date_dir if i.endswith('_matrix.xlsx')), None)
            if matrix:
                matrix_lst.append([f'{file_path}/{matrix}', f'{site}_{date}'])



            '''
            pit = next((i for i in date_dir if i.endswith('_pit.xlsx') or i.endswith('_pit_entry.xlsx')), None)
            if pit:
                pit_lst.append([f'{file_path}/{pit}', f'{site}_{date}'])

            sram = next((i for i in date_dir if i.endswith('_sram.xlsx')), None)
            if sram:
                sram_lst.append([f'{file_path}/{sram}', f'{site}_{date}'])

            pram = next((i for i in date_dir if i.endswith('_pram.xlsx')), None)
            if pram:
                pram_lst.append([f'{file_path}/{pram}', f'{site}_{date}'])

            ssa = next((i for i in date_dir if i.endswith('_SSA.xlsx')), None)
            if ssa:
                ssa_lst.append([f'{file_path}/{ssa}', f'{site}_{date}'])
            '''

#do SMP before anything else
matrix_lst = [i for i in matrix_lst if i]
#pit_lst = [i for i in pit_lst if i]
#sram_lst = [i for i in sram_lst if i]
#pram_lst = [i for i in pram_lst if i]
#ssa_lst = [i for i in ssa_lst if i]


    
#for i in sram_lst:
#    ram_scrubber(i[0], i[1]) # MUST run ram_scrubber before matrix scrubber

#for i in pram_lst:
#    ram_scrubber(i[0], i[1])

for i in matrix_lst:
    matrix_scrubber(i[0], i[1])

#for i in pit_lst:
#    pit_scrubber(i[0], i[1])

scope_list = pd.DataFrame(pd.concat(scope_list, ignore_index=True).tolist())
scope_list.to_csv('/Users/colemankane/Desktop/crrel_exports/scope_master_list.csv', index=False)