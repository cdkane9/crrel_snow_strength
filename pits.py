import pandas as pd
import numpy as np

header_cols = [
    'Site',
    'Pit ID',
    'Date',
    'Time pit open',
    'Snow depth',
    'UTME',
    'UTMN',
    'UTM zone',
    'Temp start',
    'Temp end',
    'LWC',
    'comments'
]

density_cols = [
    'top',
    'bottom',
    'A',
    'B',
    'C',
    'BulkA',
    'BulkB'
]

LWC_cols = [
    'PermA',
    'PermB',
]

temp_cols = [
    'height (cm)',
    'temp (C)'
]

strat_cols = [
    'top (cm)',
    'bottom (cm)',
    'grain max',
    'grain min',
    'grain avg',
    'type',
    'HH',
    'wetness',
    'comments',
]
poo = pd.read_excel('/Users/colemankane/Documents/BSU/CRREL Snow Strength/snow_strength_cleaning/Freeman/20250122/FRE_20250122_pit.xlsx',
                    skiprows = 1,
                    sheet_name = 'PIT')