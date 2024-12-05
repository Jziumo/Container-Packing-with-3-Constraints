import read_data
import check

def inputSolution(task, file_name, print_out=False):

    data = read_data.readData(task=task, print_out=False)
    
    file_path = './input_solution/' + file_name + '.txt'

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    solution = []
    
    with open(file_path, 'r') as file:
        for line in file:
            start_index = line.find('[')
            end_index = line.find(']')
            if start_index != -1 and end_index != -1:
                # Extract and clean the orders list
                orders_list = line[start_index+1:end_index].replace("'", "").split(', ')

                container_items = []
                container_weights = []
                container_volumes = []
                container_pallets = []

                for order_number in orders_list:
                    (order_weight, order_volume, order_pallets) = getOrder(data, order_number)
                    container_items.append(order_number)
                    container_weights.append(order_weight)
                    container_volumes.append(order_volume)
                    container_pallets.append(order_pallets)

                container_total_weight = sum(container_weights)
                container_total_volume = sum(container_volumes)
                container_total_pallets = sum(container_pallets)

                utilization_rate = ((container_total_weight / max_weight) + (container_total_volume / max_volume) + (container_total_pallets / max_pallets)) / 3
                                
                
                container = {'orders': container_items, 'weights': container_weights, 'volumes': container_volumes, 'pallets': container_pallets, 'rate': utilization_rate}

                solution.append(container)
    
    if print_out:
        if check.check(solution=solution, task=task):
            print('The solution is checked.')
            num_containers = len(solution)
            print(f'The solution has {num_containers} containers.')

    return solution

def getOrder(data, order_number):
    weight = 0
    volume = 0
    pallets = 0
    for i in range(len(data['order number'])):
        if order_number == data['order number'][i]:
            weight = data['weight'][i]
            volume = data['volume'][i]
            pallets = data['pallets'][i]
            break

    return weight, volume, pallets
        
# inputSolution(task='a', file_name='a_sm', print_out=True)