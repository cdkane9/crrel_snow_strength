import pandas as pd
import numpy as np
from pits import pit_scrubber
from ram import ram_scrubber
from matrix import matrix_scrubber

site = 'FRE'
date = '20241210'
id = f'{site}_{date}'

pit_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_pit.xlsx'
pit_scrubber(pit_path, id)

ram_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_sram.xlsx'
ram_scrubber(id, ram_path)

mat_path = f'/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/{date}/{id}_matrix.xlsx'
matrix_scrubber(mat_path, id)

