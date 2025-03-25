import pandas as pd
import numpy as np
import os
from pits import pit_scrubber
from ram import ram_scrubber
from matrix import matrix_scrubber

state = ['Colorado', 'Idaho', 'Wyoming']
data_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/20250325_testing'

for state in state:
    state_path = data_path + f'/{state}'
    state_dir = [i for i in os.listdir(state_path) if i != '.DS_Store']
    for site in state_dir:
        site_path = state_path + f'/{site}'
        site_dir = [i for i in os.listdir(site_path) if i != '.DS_Store']
        for date in site_dir:
            file_path = site_path + f'/{date}'
            date_dir = [i for i in os.listdir(file_path) if i != '.DS_Store']
print(date_dir)

'''
site = 'FRE'
date = '20241210'
id = f'{site}_{date}'

pit_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_pit.xlsx'
pit_scrubber(pit_path, id)

#ram_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_sram.xlsx'
#ram_scrubber(id, ram_path)

mat_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_matrix.xlsx'
matrix_scrubber(mat_path, id)
'''
