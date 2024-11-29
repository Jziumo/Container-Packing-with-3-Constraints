import numpy as np
import greedy_solution as greedy
import read_data


def findANeighborhood(solution):
    num_containers = len(solution)
    
    

    return

# randomly move an order from a source container to a target container
def randomMoveOrders(solution):
    num_containers = len(solution)

    # randomly select a source container
    source_index = np.random.randint(low=0, high=num_containers)
    source_container = solution[source_index]

    # randomly pick a order from the source container
    num_orders = len(source_container['orders'])
    order_index = np.random.randint(low=0, high=num_orders)
    picked_order = source_container['orders'][order_index]
    picked_weight = source_container['weights'][order_index]
    picked_volume = source_container['volumes'][order_index]
    picked_pallets = source_container['pallets'][order_index]

    # randomly select a target container (until it could add the picked order)
    # set a limit of iterations to avoid infinite loop
    changed = False
    iter_limit = 1000
    for iter_count in range (iter_limit):
        target_index = 0
        # target_index should not be the same as the source_index
        while True:
            target_index = np.random.randint(low=0, high=num_containers)
            # break the loop only if the target container is different from the source container
            if target_index != source_index:
                break;
        
        target_container = solution[target_index]
        target_weight = sum(target_container['weights'])
        target_volume = sum(target_container['volumes'])
        target_pallets = sum(target_container['pallets'])

        # check if the picked order can be moved to the target container
        if not exceedLimit(target_weight, target_volume, target_pallets, picked_weight, picked_volume, picked_pallets):
            # remove the order from the source container
            source_container['orders'].pop(order_index)
            source_container['weights'].pop(order_index)
            source_container['volumes'].pop(order_index)
            
            # add the order to the target container
            target_container['orders'].append(picked_order)
            target_container['weights'].append(picked_weight)
            target_container['volumes'].append(picked_volume)
            target_container['pallets'].append(picked_pallets)

            changed = True
            break;

    # replace the source and the target containers in the solution
    solution[source_index] = source_container
    solution[target_index] = target_container

    return solution, changed

# check if an order can be added to a container (limit constraints)
def exceedLimit(cur_weight, cur_volume, cur_pallets, add_weight, add_volume, add_pallets):
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600
    return (cur_weight + add_weight > max_weight) and (cur_volume + add_volume > max_volume) and (cur_pallets + add_pallets > max_pallets)

# df = read_data.getDataFrame(task='a')
# df['lambda'] = greedy.getOrderLambda(df, y=100)
# data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))

# solution, num_containers = greedy.greedy(task='a', data=data, print_out=False)
# print("Number of containers used:", num_containers)

# solution, changed = randomMoveOrders(solution)

# print(changed)
