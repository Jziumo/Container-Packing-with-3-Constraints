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

    return data.to_numpy()

# read_data('a')
read_data('b')