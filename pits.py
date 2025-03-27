import pandas as pd
import numpy as np

header_cols = [
    'Pit ID',#
    'Time pit open',#
    'Snow depth',#
    'UTME',#
    'UTMN',#
    'UTM zone',#
    'Temp start',#
    'Temp end',#
    'LWC', #
    'comments'
]

density_cols = [
    'top',
    'bottom',
    'A',
    'B',
    'C',
] # will add BulkA, BulkB, SWEA, SWEB later

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
    'comments'
]


def pit_scrubber(pit_path, id):
    '''
    reads in a pat to a pit sheet.  pulls out different data types and exports to .csv
    :param pit_path: path to pit
    :return: .csv of strat, LWC, density, temp, header
    '''
    print(id)
    sheet = pd.read_excel(pit_path,
                          skiprows=1,
                          sheet_name=['PIT'])

    #separate pit data and environment
    poo = sheet['PIT']
    #env = sheet['Copy of NEW ENVIORMENT']


    #pull out header data
    pit_id = id
    hs = float(poo.iloc[5, 4]) # snow depth
    open_t = poo.iloc[3,6] # time pit opened
    utme = poo.iloc[5,8] # UTM easting
    utmn = poo.iloc[5,12] # UTM northing
    utmz = poo.iloc[5,17] # UTM zone
    temp_s = poo.iloc[3,19] # temp profile start time
    temp_e = poo.iloc[3,20] # temp profile end time
    lwc_sn = poo.iloc[5,6] # LWC serial number
    cmnts = poo.iloc[0,-2] # comments/notes

    header = [
        pit_id,
        open_t,
        hs,
        utme,
        utmn,
        utmz,
        temp_s,
        temp_e,
        lwc_sn,
        cmnts

    ]
    header = pd.DataFrame([header], columns=header_cols)


    #pull out LWC
    perm = poo.iloc[9:, 6:8]
    perm.columns = LWC_cols
    perm = perm.reset_index(drop=True)


    #pull out temp profile
    temp = poo.iloc[9:, 8:10]
    temp.columns = temp_cols
    temp = temp.reset_index(drop=True)


    #pull out stratigraphy
    strat = poo.iloc[9:, 11:].dropna(how='all', axis=1)
    strat = strat.dropna(how='all', axis=0)
    strat = strat.drop(strat.columns[1], axis=1).reset_index(drop=True)
    strat.columns = strat_cols


    # pull out density profiles
    bottom_col = poo.iloc[9:, 2] # column with height of the bottom of each density sample
    first_na = bottom_col.isna().idxmax()  # index of the first instance of NaN, extent of density measurements

    #subset of density measurements (top, bottom, denA, denB, denC)
    den = poo.iloc[9:first_na, 0:6]
    den = den.drop(den.columns[1], axis=1).reset_index(drop=True) # drop column with '-' between top and bottom
    den.columns = density_cols # add column names
    den = den.astype(float)
    den[['BulkA', 'BulkB', 'SWEA', 'SWEB']] = np.nan # add placeholder columns for bulk density and SWE

    def calc_bulk(profile):
        '''
        calculates bulk density from one density profile
        :param profile: A or B
        :return: bulk density, swe
        '''
        weights = den['top'] - den['bottom']
        weighted = den[profile] * weights
        bulk_den = np.nansum(weighted) / hs
        swe = bulk_den * hs / 1000
        return bulk_den, swe


    #dealing with density profile that does not extend to ground
    den.iloc[-1, 1] = 0 # change bottom of last measurement to 0
    den.iloc[-1, 0] = den.iloc[-2, 1] # change top of last measurement to bottom of second to last measurement

    # replaces denB with average of denB and denC
    den['B'] = den.apply(lambda row: (row['B'] + row['C']) / 2 if not pd.isna(row['C']) else row['B'], axis=1)

    #call function to calculate bulk density and SWE
    bulk_A, sweA = calc_bulk('A')
    bulk_B, sweB = calc_bulk('B')

    #insert values into df
    den.loc[0, 'BulkA'] = bulk_A
    den.loc[0, 'BulkB'] = bulk_B
    den.loc[0, 'SWEA'] = sweA
    den.loc[0, 'SWEB'] = sweB

    #export all data frames to .csv
    export_path = '/Users/colemankane/Desktop/crrel_exports'

    #den.to_csv(f'{export_path}/{pit_id}_den.csv', index=False)
    #temp.to_csv(f'{export_path}/{pit_id}_temp.csv', index=False)
    strat.to_csv(f'/Users/colemankane/Desktop/flakesense/{pit_id}_strat.csv', index=False)
    #strat.to_csv(f'{export_path}/{pit_id}_strat.csv', index=False)
    #header.to_csv(f'{export_path}/{pit_id}_header.csv', index=False)
    #perm.to_csv(f'{export_path}/{pit_id}_perm.csv', index=False)

    return



