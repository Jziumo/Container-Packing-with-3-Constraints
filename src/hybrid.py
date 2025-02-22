import read_data
import greedy_solution as greedy
import exact_search

def hybrid():
    
    data = read_data.readSortedData(task='a', w=1, v=201, p=1, ascending=False, print_out=False)

    solution, num_containers = greedy.greedy(task='a', data=data, print_out=False)

    # print(num_containers)

    # sort by rates in ascending order
    sorted_solution = sorted(solution, key=lambda x : x['rate'])

    orders = []

    order_cnt = 0
    container_cnt = 0

    for i in range(num_containers):
        container = sorted_solution[i]

        for order in container['orders']:
            orders.append(order)
            order_cnt += 1

        container_cnt += 1

        if order_cnt >= 40: 
            break
    
    # print(orders)
    # print(order_cnt)
    # print(container_cnt)

    data = getOrdersData(orders)

    # print(data['weight'][0], data['weight'][49])

    optimized_num, _ = exact_search.exactSearch(task='a', data=data, print_out=True, greedy_hint=True)

    print(f'original number of containers: {container_cnt} | optimized: {optimized_num}')

    return

def getOrdersData(orders):
    original_data = read_data.readData(task='a', first_n_rows=None, print_out=False)
    size = len(original_data['order number'])

    data = {}
    data['order number'] = []
    data['weight'] = []
    data['volume'] = []
    data['pallets'] = []

    for order in orders:
        for i in range(size):
            order_num = original_data['order number'][i]

            if order_num == order:
                data['order number'].append(order_num)
                data['weight'].append(original_data['weight'][i])
                data['volume'].append(original_data['volume'][i])
                data['pallets'].append(original_data['pallets'][i])

    # sorted(data, key=lambda : )
    lambda_list = []
    w = 1
    v = 201
    p = 1
    for i in range(len(data['order number'])):
        lambda_value = data['weight'][i] * w + data['volume'][i] * v + data['pallets'][i] * p
        lambda_list.append((lambda_value, i))

    lambda_list = sorted(lambda_list)

    sorted_data = {
        'order number': [],
        'weight': [],
        'volume': [],
        'pallets': []
    }

    for _, index in lambda_list:
        sorted_data['order number'].append(data['order number'][index])
        sorted_data['weight'].append(data['weight'][index])
        sorted_data['volume'].append(data['volume'][index])
        sorted_data['pallets'].append(data['pallets'][index])
        
    return sorted_data

hybrid()
