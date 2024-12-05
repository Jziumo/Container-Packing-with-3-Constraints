
import read_data

def getRandomSolution(task, print_out=False): 

    data = read_data.readShuffledData(task=task, first_n_rows=None)

    size = len(data['order number'])

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    # a solution formed by a group of containers 
    solution = []
    container_idx = 0

    # variables used to calculate the utilization rate
    weights = []
    volumes = []
    pallets = []
    rates = []

    all_satisfied = True
    order_idx = 0

    output_message = ""

    while order_idx < size: 
        # values of each 
        container_items = []

        container_weight = 0
        container_volume = 0
        container_pallets = 0

        # fill the container until it is full or all orders are packed
        while order_idx < size: 
            if exceedLimit(container_weight, container_volume, container_pallets, data, order_idx) == False: 
                container_items.append(data['order number'][order_idx])

                container_weight += data['weight'][order_idx]
                container_volume += data['volume'][order_idx]
                container_pallets += data['pallets'][order_idx]

                order_idx += 1
            else: 
                break;

        # a container is almost full
        weights.append(container_weight)
        volumes.append(container_volume)
        pallets.append(container_pallets)

        output_message += f"Container {container_idx}:\n" 
        output_message += f"├─ Orders packed: {container_items}\n"
        output_message += f"├─ Weight: {container_weight}\n"
        output_message += f"├─ Volume: {container_volume}\n"
        output_message += f"├─ Pallets: {container_pallets}\n"
        
        # check if the container satisfies the capacity constraint
        satisfy_contraint = True
        if container_weight <= max_weight and container_volume <= max_volume and container_pallets <= max_pallets:
            output_message += "├─ (satisfies the capacity constraints)\n"
        else: 
            output_message += "└─ container is overloaded!\n"
            satisfy_contraint = False
            all_satisfied = False   
        
        # analyze the utilization rate
        utilization_rate = -1
        if satisfy_contraint:
            utilization_rate = (container_weight / max_weight + container_volume / max_volume + container_pallets / max_pallets) / 3
            rates.append(utilization_rate)
            output_message += f"└─ Average utilization rate of the container: {utilization_rate: .4f}\n"

        output_message += "\n"
        
        container = {'orders': container_items, 'weights': weights, 'volumes': volumes, 'pallets': pallets, 'rate': utilization_rate}
        solution.append(container)

        container_idx += 1
        
    output_message += "Total analysis: \n"

    output_message += f"├─ Total number of containers used: {container_idx}\n"

    # calculate the total amount 
    total_weight = sum(weights)
    total_volume = sum(volumes)
    total_pallets = sum(pallets)
    
    # calculate the utilization rate of each column
    weight_rate = total_weight / (max_weight * container_idx)
    volume_rate = total_volume / (max_volume * container_idx)
    pallets_rate = total_pallets / (max_pallets * container_idx)
    total_utilization_rate = (weight_rate + volume_rate + pallets_rate) / 3

    output_message += "├─ Utilization rate\n"
    output_message += f"│  ├─ weight rate: {weight_rate: .4f}\n"
    output_message += f"│  ├─ volume rate: {volume_rate: .4f}\n"
    output_message += f"│  ├─ pallets rate: {pallets_rate: .4f}\n"
    output_message += f"│  └─ total: {total_utilization_rate: .4f}\n"

    # output if all the containers satisfy the capacity constraint
    if all_satisfied: 
        output_message += "└─ All containers satisfy the capacity constraints.\n"
    else: 
        output_message += "└─ Some containers are overloaded!\n"

    # print and write messages

    if print_out:
        print(output_message) 
    output_path = ''
    if task == 'a':
        output_path = "./output/result_a_random.txt"
    elif task == 'b':
        output_path = "./output/result_b_random.txt"

    with open(output_path, "w") as file: 
        file.write(output_message)

    return solution, container_idx

def exceedLimit(cur_weight, cur_volume, cur_pallets, data, i):
    return cur_weight + data['weight'][i] > 45000 or cur_volume + data['volume'][i] > 3600 or cur_pallets + data['pallets'][i] > 60

def randomTest(task, test_times=100):
    sum = 0
    for i in range(test_times):
        _,num_containers = getRandomSolution(task=task, print_out=False)
        sum += num_containers
        
    average = sum / test_times
    print(f"Average number of containers in random solutions: {average: .2f}")
    return

# randomTest('b', 10000)
