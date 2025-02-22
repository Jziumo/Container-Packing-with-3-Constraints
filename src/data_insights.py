import read_data
import statistics
import matplotlib.pyplot as plt
import greedy_solution as greedy
import random_solution as rd
import solution_input

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

    # print(variance_weight, variance_volume, variance_pallets)

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

def viewOrder(task, order): 
    data = read_data.readData(task=task, first_n_rows=None, print_out=True)
    
    for i in range(len(data['order number'])):
        if order == data['order number'][i]:
            weight = data['weight'][i]
            volume = data['volume'][i]
            pallets = data['pallets'][i]
            print(f'weight: {weight}')
            print(f'volume: {volume}')
            print(f'pallets: {pallets}')
            utilization_rate = ((weight / 45000) + (volume / 3600) + (pallets / 60)) / 3
            print(f'utilization rate: {utilization_rate:.2f}')
            break

    return

def compareWithRandom(task='a'):
    data = read_data.readSortedData(task='a', w=1, v=201, p=1, first_n_rows=None)
    solution, num_containers = greedy.greedy(task=task, data=data, print_out=False)

    random_rates = []
    greedy_x = []
    random_x = []
    greedy_rates = []
    for i in range(num_containers):
        container = solution[i]
        greedy_rates.append(container['rate'])
        greedy_x.append((i + 1) / 100)

    # random_solution, random_num_containers = rd.getRandomSolution(task='a')

    # for i in range(random_num_containers):
    #     container = random_solution[i]
    #     random_rates.append(container['rate'])
    #     random_x.append((i + 1) / 100)
    sa_rates = []
    sa_x = []
    sa_solution = solution_input.inputSolution(task='a', file_name='a_sm')
    for i in range(len(sa_solution)):
        container = sa_solution[i]
        sa_rates.append(container['rate'])
        sa_x.append((i + 1) / 100)
        

    plt.scatter(greedy_x, greedy_rates, label='Greedy')
    plt.scatter(sa_x, sa_rates, label='SA')
    plt.ylabel('Utilization Rate')
    plt.title(f'Utilization Rate of Containers in Part ({task})')
    plt.legend(loc='upper right')
    plt.show()
    return
    
        

# getDataInsights(task='a')
# getDataInsights(task='b')
# viewOrder(task='a', order='74322802')
compareWithRandom()