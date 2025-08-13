import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data_dir = '/Users/colemankane/Library/CloudStorage/GoogleDrive-ColemanKane@boisestate.edu/Shared drives/2024-2025 CRREL Snow Strength/Data/Scrubbed pit strength transect data/crrel_exports'
smp_dir = '/Users/colemankane/Library/CloudStorage/GoogleDrive-ColemanKane@boisestate.edu/Shared drives/2024-2025 CRREL Snow Strength/Data/Scrubbed pit strength transect data/crrel_exports/smp_profiles_exports'

id_sites = ['FRE', 'BOG', 'BDG', 'PLT1', 'PLT2']
strat_files = [i for i in os.listdir(data_dir) if i.endswith('_strat.csv')]
strat_files = [i for i in strat_files if i.startswith(tuple(id_sites))]

for file in strat_files:
    print(file)
    id = f'{file.split('_')[0]}_{file.split('_')[1]}'
    smp_filename = id + '_smp.csv'

    try:
        smp_mat = pd.read_csv(os.path.join(data_dir, smp_filename)) # read in file containing SMP profiles
        good_profs = smp_mat['Comments'].isna() # filters out profiles with errors/overloads
        good_profs = smp_mat['Y-Coord'] == -30 # use only profiles 30cm away from pit wall
        smp_mat = smp_mat[good_profs]

        smp_sn = smp_mat['SN'].astype(int).astype(str).str.zfill(2) # create filenames for SMP profiles
        smp_pn = smp_mat['Profile #'].astype(int).astype(str).str.zfill(4)
        smp_profs = 'S' + smp_sn + 'M' + smp_pn + '.PNT_derivatives.csv'
        smp_profs = list(smp_profs)


        strat = pd.read_csv(data_dir + '/' + file) # read in strat file

        bottom = strat.index[strat['bottom_cm'] == 0][0] # find the bottom of the stratigraphy profile
        strat = strat.loc[:bottom]

        hs = strat.loc[0, 'top_cm']

        missing_obs = strat.index[strat['density_kgm3'].isna() | strat['swe_mm'].isna()].tolist()
        strat_filtered = strat.loc[missing_obs]



        for i in strat_filtered.index:
        #for i in strat.index:
            rho_to_avg = []

            top = strat_filtered.loc[i, 'top_cm']
            #top = strat.loc[i, 'top_cm']
            bottom = strat_filtered.loc[i, 'bottom_cm']
            #bottom = strat.loc[i, 'bottom_cm']
            delta = top - bottom

            top_depth = ((hs - top) + (0.2 * delta)) * 10
            bottom_depth = ((hs - bottom) - (0.2 * delta)) * 10

            for j in smp_profs:

                smp_prof = pd.read_csv(os.path.join(smp_dir, j), dtype=float)
                smp_depth = smp_prof['distance [mm]'].iloc[-1]
                smp_layer_ix = smp_prof.index[(smp_prof['distance [mm]'] >= top_depth) & (smp_prof['distance [mm]'] < bottom_depth)]
                layer_rho = smp_prof.loc[smp_layer_ix]['CR2020_density [kg/m^3]'] # all density values from layer
                if layer_rho.empty: #in cases where there are layers deeper than SMP
                    delta = np.nan
                    layer_swe = np.nan
                    layer_density = np.nan
                else:
                    avg_layer_rho = np.nanmean(layer_rho) # density of layer from one profile
                    rho_to_avg.append(avg_layer_rho)

            layer_density = np.nanmean(rho_to_avg) #average density for given layer
            #print(layer_density)
            layer_swe = layer_density * delta / 100

            strat.at[i, 'hs_cm'] = round(delta,1) # fill values in stratigraphy file
            strat.at[i, 'swe_mm'] = round(layer_swe,1)
            strat.at[i, 'density_kgm3'] = round(layer_density,1)



        strat.to_csv(data_dir + '/' + file, index=False)


    except Exception as e:
        print(e)
        print('no SMP profiles')



