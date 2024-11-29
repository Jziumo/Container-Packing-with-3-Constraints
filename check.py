def check(solution):

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600
    
    num_containers = len(solution)
    for i in range(num_containers):
        container = solution[i]
        container_weight = sum(container['weights'])
        container_volume = sum(container['volumes'])
        container_pallets = sum(container['pallets'])
        
        if container_weight > max_weight or container_volume > max_volume or container_pallets > max_pallets:
            return False

    return True