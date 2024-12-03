import read_data
import statistics
import matplotlib.pyplot as plt

def getDataInsights(task):
    data = read_data.readData(task=task, first_n_rows=None, print_out=True)

    size = len(data['order number'])

    # average number
    weights = []
    volumes = []
    pallets = []

    for i in range(size):
        weights.append(data['weight'][i])
        volumes.append(data['volume'][i])
        pallets.append(data['pallets'][i])

    average_weight = sum(weights) / size
    average_volume = sum(volumes) / size
    average_pallets = sum(pallets) / size

    variance_weight = statistics.variance(weights)
    variance_volume = statistics.variance(volumes)
    variance_pallets = statistics.variance(pallets)

    x = list(range(1, size + 1))
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    drawScatterPlot(task=task, column='Weight', max_value=max_weight, average=average_weight, x=x, val_list=weights, dot_color='blue')
    drawScatterPlot(task=task, column='Volume', max_value=max_volume, average=average_volume, x=x, val_list=volumes, dot_color='green')
    drawScatterPlot(task=task, column='Pallets', max_value=max_pallets, average=average_pallets, x=x, val_list=pallets, dot_color='orange')

    return

def drawScatterPlot(task, column, max_value, average, x, val_list, dot_color):
    plt.axhline(y=max_value, color='r', linestyle='-', label=f'max = {max_value}')
    plt.axhline(y=average, color='gray', linestyle='--', label=f'avg = {average: .2f}')
    plt.scatter(x, val_list, color=dot_color, marker='o')
    plt.title(column + f' of orders in Part ({task})')
    plt.xlabel('Orders Indice')
    plt.ylabel(column)
    plt.legend(loc='upper right')
    plt.show()
    return


# getDataInsights(task='a')
getDataInsights(task='b')