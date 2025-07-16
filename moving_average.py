import numpy as np

def mov_avg(x, y, w_size, weight=False):
    '''
    calculates moving window average of a dataset
    :param x: independent variable of a dataset
    :param y: dependent variable of a dataset
    :param w_size: window size
    :param weight: default false. whether to calculate weighted moving window average
    :return: moving average of y-values
    '''
    mov_mean = np.zeros(len(x))  # initiate array
    if not weight:
        count = 0
        for i in x:
            xlow = i - w_size / 2
            xhigh = i + w_size / 2
            Ix = np.logical_and(x > xlow, x < xhigh)
            wind_avg = np.mean(y[Ix])
            mov_mean[count] = wind_avg
            count +=1
    else:
        count = 0
        for i in x:
            xlow = i - w_size / 2
            xhigh = i + w_size / 2
            Ix = np.logical_and(x > xlow, x < xhigh)
            y_mod = y[Ix]
            weights = []
            for j in x[Ix]:
                weight = (15 / 16) * (1 - ((j - i) / (w_size / 2)) ** 2) ** 2
                weights.append(weight)
            ymod_denom = sum(weights)
            ymod_num = y_mod * weights
            ymod = sum(ymod_num) / ymod_denom
            mov_mean[count] = ymod
            count += 1
    return mov_mean