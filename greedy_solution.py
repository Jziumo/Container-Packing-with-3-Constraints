import read_data

def greedy(task, data=None, print_out=False):
    if data == None: 
        data = read_data.readSortedData(task, sort_by="volume", ascending=False, print_out=print_out)

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
    
    # boolean tags of all the orders, indicating whether they are pakced
    packed = [False] * size

    while order_idx < size: 
        # values of each 
        container_items = []

        container_weight = 0
        container_volume = 0
        container_pallets = 0

        # fill the container until it is full or all orders are packed
        while order_idx < size: 
            # print('order_idx:', order_idx)
            if packed[order_idx] == False:

                if exceedLimit(container_weight, container_volume, container_pallets, data, order_idx) == False: 
                    # pack the current order (largest value)
                    container_items.append(data['order number'][order_idx])
                    container_weight += data['weight'][order_idx]
                    container_volume += data['volume'][order_idx]
                    container_pallets += data['pallets'][order_idx]
                    packed[order_idx] = True

                    order_idx += 1
                else: 
                    # look for other smaller items that could be packed in
                    for i in range(size - 1, order_idx, -1):
                        if packed[i] == False and exceedLimit(container_weight, container_volume, container_pallets, data, i) == False:
                            # print('pack:', i)
                            container_items.append(data['order number'][i])
                            container_weight += data['weight'][i]
                            container_volume += data['volume'][i]
                            container_pallets += data['pallets'][i]
                            packed[i] = True      
                    # break the container loop
                    break;
            else:
                order_idx += 1

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
        if satisfy_contraint:
            utilization_rate = (container_weight / max_weight + container_volume / max_volume + container_pallets / max_pallets) / 3
            rates.append(utilization_rate)
            output_message += f"└─ Average utilization rate of the container: {utilization_rate: .4f}\n"

        output_message += "\n"
        
        container = {'orders': container_items, 'weight': container_weight, 'volume': container_volume, 'pallets': container_pallets}
        solution.append(container)

        container_idx += 1
        # The container loop ends here
        
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
        output_path = "./output/result_a_greedy.txt"
    elif task == 'b':
        output_path = "./output/result_b_greedy.txt"

    with open(output_path, "w") as file: 
        file.write(output_message)

    return solution, container_idx

def exceedLimit(cur_weight, cur_volume, cur_pallets, data, i):
    return cur_weight + data['weight'][i] > 45000 or cur_volume + data['volume'][i] > 3600 or cur_pallets + data['pallets'][i] > 60

def getOrderLambda(df, x=1, y=1, z=1): 
    # coefficient for each attribute
    return df['Weight (lbs)'] * x + df['Volume (in3)'] * y + df['Pallets'] * z

df = read_data.getDataFrame(task='b')
df['lambda'] = getOrderLambda(df)
data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))

_,num_containers = greedy(task='b', data=data, print_out=False)
print("Number of containers used:", num_containers)