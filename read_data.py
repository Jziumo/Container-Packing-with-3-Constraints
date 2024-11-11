import pandas as pd

data_1a = "./data/Term project data 1a.csv"
data_1b = "./data/Term project data 1b.csv"

def read_data(task) :
    file_read = ''
    if task == 'a':
        file_read = data_1a
    elif task == 'b':
        file_read = data_1b

    data = pd.read_csv(file_read, usecols=[0, 1, 2, 3])

    # drop the missing values
    data = data.dropna(subset=[data.columns[0]])

    print("The rows and columns of the data:", data.shape[0], 'x', data.shape[1])

    # @todo 将data 改为map式的
    map = {}
    map['order number'] = [str(int(order)) for order in data['Order Number'].tolist()]
    map['weight'] = [int(weight) for weight in data['Weight (lbs)'].tolist()]
    map['volume'] = [int(volume) for volume in data['Volume (in3)'].tolist()]
    map['pallets'] = [int(pallets) for pallets in data['Pallets'].tolist()]

    return map

read_data('a')
# read_data('b')