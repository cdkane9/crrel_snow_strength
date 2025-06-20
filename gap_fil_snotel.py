import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt

def gap_fill(caca, snotel, start, end, param, shift, dategap=False, scatter=False):
    '''
    Fills gaps in weather station data using nearby snotel stations
    :param caca: weather station data
    :param snotel: snotel data.  must have same time step as wx station
    :param start: gap start
    :param end: gap end
    :param param: parameter to fill
    :return:
    '''

    sgap = pd.Timestamp(start)
    egap = pd.Timestamp(end)
    if dategap:
        # add in missing dates
        full_idx = pd.date_range(
            start=caca.index.min(),
            end=caca.index.max(),
            freq='15min',
        )
        caca = caca.reindex(full_idx).interpolate(method='index')

    # align two datasets on common indices
    common_index = caca.index.intersection(snotel.index)
    caca_aln = caca.loc[common_index]
    stl_aln = snotel.loc[common_index]

    #subset where both datasets are not nan
    mask = np.isfinite(caca_aln[param]) & np.isfinite(stl_aln[param])
    caca_aln = caca_aln[mask]
    stl_aln = stl_aln[mask]

    # define model to go from snotel HS to site HS
    m, b = np.polyfit(stl_aln[param], caca_aln[param], 1)
    rmse = np.sqrt(mean_squared_error(caca_aln[param],
                                      m * stl_aln[param] + b))

    # if HS, gap fill based on linear model coeff and values at start/end of gap
    if param == 'hs_cm':
        start_gap = caca_aln.loc[sgap, param] - snotel.loc[sgap, param]
        end_gap = caca_aln.loc[egap, param] - snotel.loc[egap, param]

        stl_fill = snotel[(snotel.index >= sgap) & (snotel.index < egap)].copy()
        if shift == 'avg':
            avg_diff = (start_gap + end_gap) / 2
            fill = m * stl_fill[param] + avg_diff
            #print(avg_diff)
        elif shift == 'start':
            fill = (m * stl_fill[param] + start_gap)
            #print(start_gap)
        elif shift == 'end':
            fill = (m * stl_fill[param] + end_gap)
            #print(end_gap)
        else:
            fill = (m * stl_fill[param] + b)
    else:
        stl_fill = snotel[(snotel.index >= sgap) & (snotel.index < egap)].copy()
        fill = m * stl_fill[param] + b

    caca.loc[sgap:egap, param] = fill
    caca.loc[sgap:egap, 'flag'] = 1
    if scatter:
        plt.scatter(stl_aln[param], caca_aln[param])
        plt.xlabel('Snotel')
        plt.ylabel('Site')
        plt.show()

    return caca, m, b, rmse

