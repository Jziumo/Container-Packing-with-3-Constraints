import pandas as pd

data_1a_path = "./data/Term project data 1a.csv"
data_1b_path = "./data/Term project data 1b.csv"

# column names mapping to the original csv file
col_names = {"order number": "Order Number", "weight": "Weight (lbs)", "volume": "Volume (in3)", "pallets": "Pallets", "lambda": "lambda"}

def readData(task, first_n_rows = None, print_out=False):
    file_path = ''
    if task == 'a':
        file_path = data_1a_path
    elif task == 'b':
        file_path = data_1b_path

    data = read(file_path)

    # get the first n rows if specified
    if first_n_rows is not None:
        data = data.head(first_n_rows)

    if print_out: 
        print("The rows and columns of the data:", data.shape[0], 'x', data.shape[1])

    map = getMap(data)

    return map

# get sorted data
def readSortedData(task, sort_by='weight', ascending=True, first_n_rows = None, print_out=False): 
    file_path = ''
    if task == 'a':
        file_path = data_1a_path
    elif task == 'b':
        file_path = data_1b_path

    data = read(file_path)
    
    # sort the data frame
    data = sort(data, sort_by=sort_by, ascending=ascending)

    # get the first n rows if specified
    if first_n_rows is not None:
        data = data.head(first_n_rows)

    if print_out:
        print("The rows and columns of the data:", data.shape[0], 'x', data.shape[1])

    map = getMap(data)

    return map

# get shuffled data
def readShuffledData(task, first_n_rows = None, print_out=False): 
    file_path = ''
    if task == 'a':
        file_path = data_1a_path
    elif task == 'b':
        file_path = data_1b_path

    data = read(file_path)

    # shuffle the data frame
    data = shuffle(data)

    # get the first n rows if specified
    if first_n_rows is not None:
        data = data.head(first_n_rows)

    if print_out:
        print("The rows and columns of the data:", data.shape[0], 'x', data.shape[1])

    map = getMap(data)

    return map

# map the task and file path
def getDataFrame(task): 
    file_path = ''
    if task == 'a':
        file_path = data_1a_path
    elif task == 'b':
        file_path = data_1b_path

    data = read(file_path)
    return data
    
# read file and return the data frame of the .csv file
def read(file_path):
    data = pd.read_csv(file_path, usecols=[0, 1, 2, 3])
    # drop the missing values
    data = data.dropna(subset=[data.columns[0]])
    return data

# convert the data frame to a python list (map)
def getMap(data):
    map = {}
    map['order number'] = [str(int(order)) for order in data['Order Number'].tolist()]
    map['weight'] = [int(weight) for weight in data['Weight (lbs)'].tolist()]
    map['volume'] = [int(volume) for volume in data['Volume (in3)'].tolist()]
    map['pallets'] = [int(pallets) for pallets in data['Pallets'].tolist()]
    return map

# sort the data frame and return
def sort(data, sort_by='weight', ascending=True): 
    sort_by = col_names[sort_by]
    data.sort_values(by=sort_by, ascending=ascending, inplace=True)
    return data

# shuffle the data frame and return
def shuffle(data): 
    return data.sample(frac=1)

# extract data from start (inclusive) to end (exclusive) index
def extract(data, start, end): 
    return data.iloc[start:end]

# readData('b', print_out=True)