import numpy as np
import greedy_solution as greedy
import read_data

# randomly swap two orders in two different containers in the solution
def randomSwapOrders(solution, penalty_allowed=True):
    num_containers = len(solution)
    
    # randomly select 2 different containers
    a_idx = 0
    b_idx = 0
    while a_idx == b_idx:
        a_idx = np.random.randint(low=0, high=num_containers)
        b_idx = np.random.randint(low=0, high=num_containers)

    a_container = solution[a_idx]
    b_container = solution[b_idx]
    
    # randomly pick a order from each container, respectively
    a_num_orders = len(a_container['orders'])
    b_num_orders = len(b_container['orders'])

    changed = False;
    iter_limit = 1000
    for iter_count in range (iter_limit):
        a_order_idx = np.random.randint(low=0, high=a_num_orders)
        b_order_idx = np.random.randint(low=0, high=b_num_orders)

        if penalty_allowed: 
            a_container, b_container = swap(a_container, b_container, a_order_idx, b_order_idx)
            changed = True
            break;
        else:
            if canSwap(a_container, b_container, a_order_idx, b_order_idx): 
                a_container, b_container = swap(a_container, b_container, a_order_idx, b_order_idx)
                changed = True
                break;
    
    # replace two containers in the solution
    solution[a_idx] = a_container
    solution[b_idx] = b_container

    return solution, changed

# randomly move an order from a source container to a target container
def randomMoveOrders(solution, penalty_allowed=True):
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
    return (cur_weight + add_weight > max_weight) or (cur_volume + add_volume > max_volume) or (cur_pallets + add_pallets > max_pallets)

def canSwap(a_container, b_container, a_order_idx, b_order_idx): 
    a_picked_weight = a_container['weights'][a_order_idx]
    a_picked_volume = a_container['volumes'][a_order_idx]
    a_picked_pallets = a_container['pallets'][a_order_idx]

    b_picked_weight = b_container['weights'][b_order_idx]
    b_picked_volume = b_container['volumes'][b_order_idx]
    b_picked_pallets = b_container['pallets'][b_order_idx]

    a_weight = sum(a_container['weights'])
    a_volume = sum(a_container['volumes'])
    a_pallets = sum(a_container['pallets'])

    b_weight = sum(b_container['weights'])
    b_volume = sum(b_container['volumes'])
    b_pallets = sum(b_container['pallets'])

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600    
    
    c1 = (a_weight - a_picked_weight + b_picked_weight <= max_weight)
    c2 = (a_volume - a_picked_volume + b_picked_volume <= max_volume)
    c3 = (a_pallets - a_picked_pallets + b_picked_pallets <= max_pallets)
    c4 = (b_weight - b_picked_weight + a_picked_weight <= max_weight)
    c5 = (b_volume - b_picked_volume + a_picked_volume <= max_volume)
    c6 = (b_pallets - b_picked_pallets + a_picked_pallets <= max_pallets)

    return c1 and c2 and c3 and c4 and c5 and c6

# swap two orders in two containers
def swap(a_container, b_container, a_order_idx, b_order_idx): 
    a_picked_order = a_container['orders'][a_order_idx]
    a_picked_weight = a_container['weights'][a_order_idx]
    a_picked_volume = a_container['volumes'][a_order_idx]
    a_picked_pallets = a_container['pallets'][a_order_idx]

    b_picked_order = b_container['orders'][b_order_idx]
    b_picked_weight = b_container['weights'][b_order_idx]
    b_picked_volume = b_container['volumes'][b_order_idx]
    b_picked_pallets = b_container['pallets'][b_order_idx]

    a_container['orders'].pop(a_order_idx)
    a_container['weights'].pop(a_order_idx)
    a_container['volumes'].pop(a_order_idx)
    a_container['pallets'].pop(a_order_idx)
    b_container['orders'].pop(b_order_idx)
    b_container['weights'].pop(b_order_idx)
    b_container['volumes'].pop(b_order_idx)
    b_container['pallets'].pop(b_order_idx)

    # add
    a_container['orders'].append(b_picked_order)
    a_container['weights'].append(b_picked_weight)
    a_container['volumes'].append(b_picked_volume)
    a_container['pallets'].append(b_picked_pallets)
    b_container['orders'].append(a_picked_order)
    b_container['weights'].append(a_picked_weight)
    b_container['volumes'].append(a_picked_volume)
    b_container['pallets'].append(a_picked_pallets)

    return a_container, b_container

# df = read_data.getDataFrame(task='a')
# df['lambda'] = greedy.getOrderLambda(df, y=100)
# data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))

# solution, num_containers = greedy.greedy(task='a', data=data, print_out=False)
# print("Number of containers used:", num_containers)

# solution, changed = randomSwapOrders(solution)

# # solution, changed = randomMoveOrders(solution)

# print(changed)
