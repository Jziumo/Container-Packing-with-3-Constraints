import greedy_solution as greedy
import read_data

def check(solution, task):

    correct_orders_num = 0
    if task == 'a':
        correct_orders_num = 690
    elif task == 'b':
        correct_orders_num = 1000
    

    max_pallets = 60
    max_weight = 45000
    max_volume = 3600
    
    num_containers = len(solution)
    ordersCount = {}
    total_orders_num = 0

    for i in range(num_containers):
        container = solution[i]
        container_weight = sum(container['weights'])
        container_volume = sum(container['volumes'])
        container_pallets = sum(container['pallets'])

        for order in container['orders']:
            ordersCount[order] = ordersCount.get(order, 0) + 1
            total_orders_num += 1
        
        if container_weight > max_weight or container_volume > max_volume or container_pallets > max_pallets:
            return False

    for order in ordersCount.keys():
        if ordersCount[order] > 1:
            print('here2')
            return False
        
    if correct_orders_num != total_orders_num:
        print('here3')
        return False

    return True
