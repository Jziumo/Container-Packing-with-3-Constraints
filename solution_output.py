

def outputSolution(solution, file_name):
    num_containers = len(solution)

    output_path = './output/' + file_name + '.txt'

    output_message = ''

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    weights = []
    volumes = []
    pallets = []

    all_satisfied = True
    
    with open(output_path, 'w') as f:
        f.write('')

    for i in range(num_containers):
        container = solution[i]

        container_idx = i
        container_items = container['orders']
        container_total_weight = sum(container['weights'])
        container_total_volume = sum(container['volumes'])
        container_total_pallets = sum(container['pallets'])

        weights.append(container_total_weight)
        volumes.append(container_total_volume)
        pallets.append(container_total_pallets)

        output_message += f"Container {container_idx}:\n" 
        output_message += f"├─ Orders packed: {container_items}\n"
        output_message += f"├─ Weight: {container_total_weight}\n"
        output_message += f"├─ Volume: {container_total_volume}\n"
        output_message += f"├─ Pallets: {container_total_pallets}\n"

        # check if the container satisfies the capacity constraint
        satisfy_contraint = True
        if container_total_weight <= max_weight and container_total_volume <= max_volume and container_total_pallets <= max_pallets:
            output_message += "├─ (satisfies the capacity constraints)\n"
        else: 
            output_message += "└─ container is overloaded!\n"
            satisfy_contraint = False
            all_satisfied = False   
        
        # analyze the utilization rate
        utilization_rate = -1
        if satisfy_contraint:
            utilization_rate = (container_total_weight / max_weight + container_total_volume / max_volume + container_total_pallets / max_pallets) / 3
            # rates.append(utilization_rate)
            output_message += f"└─ Average utilization rate of the container: {utilization_rate: .4f}\n"

        output_message += "\n"

    output_message += "Total analysis: \n"

    output_message += f"├─ Total number of containers used: {container_idx + 1}\n"

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

    with open(output_path, 'a') as f:
        f.write(output_message)

