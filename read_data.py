import pandas as pd

data_1a_path = "./data/Term project data 1a.csv"
data_1b_path = "./data/Term project data 1b.csv"

def readData(task, first_n_rows = None) :
    file_path = ''
    if task == 'a':
        file_path = data_1a_path
    elif task == 'b':
        file_path = data_1b_path

    data = pd.read_csv(file_path, usecols=[0, 1, 2, 3])

    # drop the missing values
    data = data.dropna(subset=[data.columns[0]])

    # get the first n rows if specified
    if first_n_rows is not None:
        data = data.head(first_n_rows)

    print("The rows and columns of the data:", data.shape[0], 'x', data.shape[1])

    map = {}
    map['order number'] = [str(int(order)) for order in data['Order Number'].tolist()]
    map['weight'] = [int(weight) for weight in data['Weight (lbs)'].tolist()]
    map['volume'] = [int(volume) for volume in data['Volume (in3)'].tolist()]
    map['pallets'] = [int(pallets) for pallets in data['Pallets'].tolist()]

    return map


readData('a')
# read_data('b')