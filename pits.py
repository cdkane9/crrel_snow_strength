import pandas as pd
import numpy as np
import os

export_path = '/Users/colemankane/Desktop/crrel_exports'


site_coords = {'BMO': [509875, 4817493, '12T'],
               'TPO': [559105, 4852195, '12T'],
               'FCO': [511490, 4802204, '12T'],
               'CCO': [513075, 4815428, '12T'],
               'FRE': [4866131, 604178, '11T'],
               'BDG': [4983225, 568300, '11T'],
               'BOG': [4845307, 573179, '11T'],
               'MCSST': [4865185, 607084, '11T'],
               'JPLMet': [4417691, 424547, '13S'],
               'FEFHQ': [4417566, 424436, '13S'],
               'FST': [4413544, 425788, '13S'],
               'LFMet': [4416150, 425293, '13S'],
               'AM' : [4412425, 426178, '13S'],
               'SLMet': [425729, 4419946, '13S']
               }


header_cols = [
    'Pit ID',#
    'Site',
    'Date',
    'Time pit open',#
    'Snow depth_cm',#
    'SWE_A_mm',
    'SWE_B_mm',
    'UTME',#
    'UTMN',#
    'UTM zone',#
    'Temp start',#
    'Temp end',#
    'LWC', #
    'comments'
] #ADD DATE COLUMN, state, site,

density_cols = [
    'top_cm',
    'bottom_cm',
    'A_kgm-3',
    'B_kgm-3',
    'C_kgm-3',
] # will add BulkA, BulkB, SWEA, SWEB later

LWC_cols = [
    'PermA',
    'PermB',
] # add device and SN here

temp_cols = [
    'height_cm',
    'temp_C'
]

strat_cols = [
    'top_cm',
    'bottom_cm',
    'grain max_mm',
    'grain min_mm',
    'grain avg_mm',
    'type',
    'HH',
    'wetness',
    'comments',
    'hs_cm',
    'swe_mm',
    'density_kgm3'
]

def pit_scrubber(pit_path, id):
    '''
    reads in a pat to a pit sheet.  pulls out different data types and exports to .csv
    :param pit_path: path to pit
    :return: .csv of strat, LWC, density, temp, header
    '''
    error_lst = []
    print(pit_path)
    print(id)
    site = id.split('_')[0]
    date = id.split('_')[1]



    try:
        sheet = pd.read_excel(pit_path,
                              skiprows=1,
                              sheet_name=['PIT'])


        #separate pit data and environment
        poo = sheet['PIT']
        #env = sheet['Copy of NEW ENVIORMENT']

        # pull out header data
        pit_id = id
        hs = float(poo.iloc[5, 4])  # snow depth
        open_t = poo.iloc[3, 6]  # time pit opened
        date = poo.iloc[0,6]
        utme = poo.iloc[5, 8]  # UTM easting
        utmn = poo.iloc[5, 12]  # UTM northing
        utmz = poo.iloc[5, 17]  # UTM zone
        temp_s = poo.iloc[3, 19]  # temp profile start time
        temp_e = poo.iloc[3, 20]  # temp profile end time
        lwc_sn = poo.iloc[5, 6]  # LWC serial number
        cmnts = poo.iloc[0, -2]  # comments/notes

        if type(utme) == float: #
            utme, utmn, utmz = site_coords[site]

        if pit_path.split('_')[-3] == 'TS':
            pit_id = f"{site}_{date}_TS_{open_t}"
            print('TIME SERIES')

        #pull out LWC
        perm = poo.iloc[9:, 6:8]
        perm.columns = LWC_cols
        if not perm.empty:
            perm = perm.reset_index(drop=True)
            perm['SN'] = lwc_sn
            #perm.to_csv(f'{export_path}/{pit_id}_perm.csv', index= False)

        #pull out temp profile
        temp = poo.iloc[9:, 8:10]
        temp.columns = temp_cols
        # add start and end time
        temp.loc[0, 't_start'] = temp_s
        temp.loc[0, 't_end'] = temp_s

        if not temp.empty:
            temp = temp.reset_index(drop=True)
            temp.loc[0, 'date'] = date
            # temp.to_csv(f'{export_path}/{pit_id}_temp.csv', index=False)
        else:
            pass


        #pull out stratigraphy
        drop_cols = [1, 4, 6, 12, 13, 14, 15, 16, 17, 18, 19] # columns that will always be NaN
        strat = poo.iloc[9:, 11:34] # stratigraphy section

        if not strat.empty:
            try:
                strat = strat.dropna(how='all').reset_index(drop=True) # drop rows of all NaN
                strat = strat.drop(columns=strat.columns[drop_cols]) # drop cols of all NaN
                strat.columns = strat_cols # rename columns
                strat_na = strat['bottom_cm'].isna().idxmax() # find ground
                strat = strat.iloc[:strat_na, :] # truncate data frame to just stratigraphy

                # calculate swe from density or density from swe
                if strat['swe_mm'].isna().all():
                    strat['swe_mm'] = strat['density_kgm3'] * strat['hs_cm'] / 100
                    strat['swe_mm'] = strat['swe_mm'].astype(float)
                    strat['swe_mm'] = strat['swe_mm'].round(0)

                elif strat['density_kgm3'].isna().all():
                    strat['density_kgm3'] = round(strat['swe_mm'] * 100 / strat['hs_cm'], 0)

                else:
                    pass

                strat.loc[0, 'date'] = date

                #strat.to_csv(f'{export_path}/{pit_id}_strat.csv', index=False)

            except Exception as e:
                error_lst.append([pit_path, id, e])

        else:
            pass

        # pull out density profiles
        bottom_col = poo.iloc[9:, 2] # column with height of the bottom of each density sample
        first_na = bottom_col.isna().idxmax()  # index of the first instance of NaN, extent of density measurements

        #subset of density measurements (top, bottom, denA, denB, denC)
        den = poo.iloc[9:first_na, 0:6]
        den = den.drop(den.columns[1], axis=1).reset_index(drop=True) # drop column with '-' between top and bottom
        den.columns = density_cols # add column names
        den = den.astype(float)
        den[['BulkA_kgm-3', 'BulkB_kgm-3', 'SWEA_mm', 'SWEB_mm']] = np.nan # add placeholder columns for bulk density and SWE

        def calc_bulk(profile):
            '''
            calculates bulk density from one density profile
            :param profile: A or B
            :return: bulk density, swe
            '''
            weights = den['top_cm'] - den['bottom_cm']
            weighted = den[profile] * weights
            bulk_den = np.nansum(weighted) / den.loc[0, 'top_cm']
            swe = round(bulk_den * den.loc[0, 'top_cm'] / 1000, 1)
            return round(bulk_den, 0), swe * 10


        #dealing with density profile that does not extend to ground

        den.iloc[-1, 1] = 0 # change bottom of last measurement to 0
        if first_na != 10: # in case one density measurement was made from surface to ground
            den.iloc[-1, 0] = den.iloc[-2, 1] # change top of last measurement to bottom of second to last measurement

        # replaces denB with average of denB and denC
        den['B_kgm-3'] = den.apply(lambda row: (row['B_kgm-3'] + row['C_kgm-3']) / 2 if not pd.isna(row['C_kgm-3']) else row['B_kgm-3'], axis=1)


        #call function to calculate bulk density and SWE
        bulk_A, sweA = calc_bulk('A_kgm-3')
        bulk_B, sweB = calc_bulk('B_kgm-3')

        #insert values into df
        den.loc[0, 'BulkA_kgm-3'] = bulk_A
        den.loc[0, 'BulkB_kgm-3'] = bulk_B
        den.loc[0, 'SWEA_mm'] = sweA
        den.loc[0, 'SWEB_mm'] = sweB

        den.to_csv(f'{export_path}/{id}_den.csv', index=False)


        header = [
            pit_id,
            site,
            date,
            open_t,
            hs,
            sweA,
            sweB,
            utme,
            utmn,
            utmz,
            temp_s,
            temp_e,
            lwc_sn,
            cmnts

        ]

        header = pd.DataFrame([header], columns=header_cols)
        header.fillna(str('N/O'), inplace=True)
        #header.to_csv(f'/Users/colemankane/Desktop/crrel_exports/{pit_id}_summary.csv', index=False)



    except Exception as e:
        print(e)
        error_lst.append([pit_path, id, e])

    error_lst = pd.DataFrame(error_lst)
    error_lst.to_csv('/Users/colemankane/Desktop/strat_err.csv', mode='a')
    return


prac_path = '/Users/colemankane/Documents/BSU/CRREL Snow Strength/field_data/Colorado/Sites/AM/20250205/AM_20250205_pit.xlsx'
prac_id = 'AM_20250205'

#pit_scrubber(prac_path, prac_id)



