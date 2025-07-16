import pandas as pd
#import numpy as np
import os
from pits import pit_scrubber
#from ssa import ssa_scrubber
#from ram import ram_scrubber
#from matrix import matrix_scrubber, scope_list
from transects import transect_scrubber


state = ['Colorado']#, 'Idaho']
data_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data'

trans_end = ['HStransect.xlsx', 'HStransectA.xlsx', 'HStransectB.xlsx',
             'HStransectRadar1.xlsx', 'HStransectRadar2.xlsx', 'HStransectJPL1.xlsx', 'HStransectJPL2.xlsx', 'HStransectJPLA.xlsx',
             ]

matrix_lst = []
pit_lst = []
sram_lst = []
pram_lst = []
ssa_lst = []
transect_lst = []

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


            matrix = [i for i in date_dir if i.endswith('_matrix.xlsx')]
            if matrix:
                matrix_lst.append([f'{file_path}/{matrix}', f'{site}_{date}'])

            pit = [i for i in date_dir if i.endswith('_pit.xlsx') or i.endswith('_pit_entry.xlsx')]
            if pit:
                for pit in pit:
                    pit_lst.append([f'{file_path}/{pit}', f'{site}_{date}'])

            sram = [i for i in date_dir if i.endswith('_sram.xlsx')]

            for s in sram:
                sram_lst.append([f'{file_path}/{s}', f'{site}_{date}'])

            pram = [i for i in date_dir if i.endswith('_pram.xlsx')]
            for p in pram:
                pram_lst.append([f'{file_path}/{p}', f'{site}_{date}'])

            ssa = [i for i in date_dir if i.endswith('_SSA.xlsx')]
            for x in ssa:
                ssa_lst.append([f'{file_path}/{x}', f'{site}_{date}'])

            trans = [i for i in date_dir if i.split('_')[-1] in trans_end]
            trans = [i for i in trans if not i.startswith('~$')]
            for t in trans:
                transect_lst.append([f'{file_path}/{t}', f'{site}_{date}'])


#do SMP before anything else
#matrix_lst = [i for i in matrix_lst if i]
#pit_lst = [i for i in pit_lst if i]
#sram_lst = [i for i in sram_lst if i]

#pram_lst = [i for i in pram_lst if i]
#ssa_lst = [i for i in ssa_lst if i]
transect_lst = [i for i in transect_lst if i]
    
#for i in sram_lst:
#    ram_scrubber(i[0], i[1]) # MUST run ram_scrubber before matrix scrubber

#for i in pram_lst:
#    ram_scrubber(i[0], i[1])

#for i in matrix_lst:
#    matrix_scrubber(i[0], i[1])

#for i in pit_lst:
#   pit_scrubber(i[0], i[1])

#for i in ssa_lst:
#    ssa_scrubber(i[0], i[1])

for i in transect_lst:
    transect_scrubber(i[0], i[1])

#scope_list = pd.DataFrame(pd.concat(scope_list, ignore_index=True).tolist())
#scope_list.to_csv('/Users/colemankane/Desktop/crrel_exports/scope_master_list.csv', index=False)