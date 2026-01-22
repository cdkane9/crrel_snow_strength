'''
All crusts measured with SMP were manually delineated in all profiles.
    The actual depth of the crust in each profile were recorded in the
    'smp_crust_mastersheet' file.  This script goes through each of the
    profiles in the document and calculates bulk density,
    max/mean/min hardness of each crust then exports as a new data file
'''
import pandas as pd
import numpy as np
import os

path_in = '/Users/colemankane/Desktop/smp_crust_mastersheet.csv'
master = pd.read_csv(path_in)

# path to all SMP derivatives
smp_dervs_path = '/Users/colemankane/Library/CloudStorage/GoogleDrive-ColemanKane@boisestate.edu/Shared drives/2024-2025 CRREL Snow Strength/Data/Scrubbed pit_strength_transect data/crrel_exports/smp_profiles_exports'

# place holder columns
master['density_kgm3'] = np.zeros(len(master))
master['avg_smp_N'] = np.zeros(len(master))
master['max_smp_N'] = np.zeros(len(master))

def look_up(df, row):
    '''
    calculates the density and force across manually delineated crust boundaries
    :return: density, max/mean force across each crust
    '''
    # define the top and bottom of the measured crust
    top = df['top_depth_mm'][row]
    bot = df['bot_depth_mm'][row]
    id = df['smp_id'][row].replace('_samples.csv', '_derivatives.csv')

    # read in SMP profile
    smp_prof = pd.read_csv(os.path.join(smp_dervs_path, id))

    # filter to top and bottom defined above
    crust_ix = smp_prof.index[(smp_prof['distance [mm]'] >= top) & (smp_prof['distance [mm]'] < bot)]

    # calculate bulk density across the crust
    crust_rho = np.mean(smp_prof['CR2020_density [kg/m^3]'][crust_ix])

    # calculate avg. hardness across crust
    crust_mean = np.mean(smp_prof['force_median [N]'][crust_ix])

    # calculate max hardness across crust
    crust_max = np.max(smp_prof['force_median [N]'][crust_ix])

    return crust_rho, crust_mean, crust_max

# find indices where crust was observed in SMP profile
obs_ix = master.index[master['present [0/1]'] == 1]

# iterate through obs_ix and store in associated column
for i in obs_ix:
    master['density_kgm3'][i] = look_up(master, i)[0]
    master['avg_smp_N'][i] = look_up(master, i)[1]
    master['max_smp_N'][i] = look_up(master, i)[2]

master.to_csv('/Users/colemankane/Desktop/smp_crust_mastersheet_calculated.csv')
