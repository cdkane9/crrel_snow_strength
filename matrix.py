import pandas as pd



def matrix_scrubber(matrix_path, id):
    '''
    reads in a hardness matrix file and produces .csv for each data type
    :param matrix_path: where to find matrix
    :return: none, exports to .csv's
    '''

    matrix = pd.read_excel(matrix_path,
                           skiprows=3)

    def get_index(type):
        '''
        finds the indices of different strength measurements
        :param type: str, data type, smp, force_ram, snow scope, etc.
        :return: series of indicies
        '''
        ix = matrix['Data Type'] == type
        return matrix[ix]

    smp = get_index('SMP')
    fscope = get_index('Force_Scope')
    fram = get_index('Force_Std_Ram')
    scope = get_index('SnowScope')

    export_path = '/Users/colemankane/Desktop/crrel_exports'
    smp.to_csv(f'{export_path}/{id}_smp.csv', index=False)
    fscope.to_csv(f'{export_path}/{id}_fscope.csv', index=False)
    fram.to_csv(f'{export_path}/{id}_fram.csv', index=False)
    scope.to_csv(f'{export_path}/{id}_scope.csv', index=False)




