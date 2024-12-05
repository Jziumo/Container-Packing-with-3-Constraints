import numpy as np
import math
import greedy_solution as greedy
import read_data
import random_solution
import check
import solution_output


def simulatedAnnealing(task, solution=None, num_iter = 100000, print_out=False, order_repeat_limit=75, cooling_rate=0.98, initial_temperature=100000000):
    

    initial_num_containers = 114514
    if solution == None:
        w = 1
        v = 1
        p = 1

        if task == 'a':
            w = 1
            v = 201
            p = 1
        elif task == 'b':
            w = 5
            v = 153
            p = 45

        data = read_data.readSortedData(task=task, w=w, v=v, p=p, ascending=False, print_out=False)
        solution, initial_num_containers = greedy.greedy(task=task, data=data, print_out=False)
    else:
        initial_num_containers = len(solution)

    output_path = './output/result_' + task + '_SM.txt'

    with open(output_path, 'w') as file:
        file.write("")

    ordersCount = {}
    order_repeat_limit = 75
    containersBlocked = []

    # record the best value
    temperature = initial_temperature
    initial_rate = getSolutionUtilizationRate(solution)
    current_rate = initial_rate
    current_num_containers = len(solution)

    beat_best = False

    for iter_cnt in range(num_iter):
        iter_info = ""

        solution = sorted(solution, key=lambda x:x['rate'])

        # current number of container
        num_containers = len(solution)

        if num_containers <= 2: 
            break

        # store the previous solution
        solutionTemp = solution.copy()

        # containerM: container with min utilization rate
        containerM = solution[0]
        rateM = containerM['rate']

        for i in range(len(containerM['orders'])):
            order = containerM['orders'][i]
            ordersCount[order] = ordersCount.get(order, 0) + 1

        containerMSatisfied = True
        for i in range(len(containerM['orders'])):
                
            order = containerM['orders'][i]
            if order in ordersCount and ordersCount[order] > order_repeat_limit:
                containersBlocked.append(containerM)
                solution.pop(0)
                num_containers = len(solution)
                # when any container is blocked, the solution must update
                current_rate = getSolutionUtilizationRate(solution)
                current_num_containers = num_containers
                containerMSatisfied = False
                break;
        
        if not containerMSatisfied: 
            continue

        # variable that note whether changes occur
        changed = False

        # containerR: a random container in the solution heap
        # solution heap must contain more than two containers
        containerR = solution[1]
        rateR = containerR['rate']
        
        # while a random container that can place orders or 
        find_limit = 1000
        find_cnt = 0
        while find_cnt < find_limit:
            # iterate a new random container finding
            # randomly select a container
            random_index = np.random.randint(1, num_containers)

            containerR = solution[random_index]

            # iterate each container in the containerM
            for idxM in range(len(containerM['orders'])):
                # order_idx = np.random.randint(0, len(containerR))
                
                order = containerM['orders'][idxM]
                weight = containerM['weights'][idxM]
                volume = containerM['volumes'][idxM]
                pallets = containerM['pallets'][idxM]

                containerRWeight = sum(containerR['weights'])
                containerRVolume = sum(containerR['volumes'])
                containerRPallets = sum(containerR['pallets'])

                # if it can be added to this random container, then add it
                if not exceedLimit(containerRWeight, containerRVolume, containerRPallets, weight, volume, pallets):
                    # add the order to the containerR
                    containerR['orders'].append(order)
                    containerR['weights'].append(weight)
                    containerR['volumes'].append(volume)
                    containerR['pallets'].append(pallets)

                    rateR = getContainerUtilizationRate(containerR)
                    
                    # remove that order in the container with min rate
                    containerM['orders'].pop(idxM)
                    containerM['weights'].pop(idxM)
                    containerM['volumes'].pop(idxM)
                    containerM['pallets'].pop(idxM)

                    rateM = getContainerUtilizationRate(containerM)
                    
                    solution.pop(random_index)
                    solution.pop(0)

                    # add the containers back to the heap
                    solution.append(containerR)
                    if len(containerM['orders']) > 0:
                        solution.append(containerM)

                    changed = True
                    
                    iter_info += 'M-->R! containerM:' + str(containerM['orders']) + ' | containerR:' + str(containerR['orders'])

                    # if something in containerM can be directly added to this containerR, then break this loop (stop iterating next order in containerM)
                    break;
                else: 
                    # if the order j in containerM cannot be added to containerR, then try to swap with some order in containerR
                    for idxR in range(len(containerR['orders'])):
                        if canSwap(containerM, containerR, idxM, idxR):
                            containerM, containerR = swap(containerM, containerR, idxM, idxR)
                            
                            rateM = getContainerUtilizationRate(containerM)
                            rateR = getContainerUtilizationRate(containerR)

                            solution.pop(random_index)
                            solution.pop(0)
                            solution.append(containerM)
                            solution.append(containerR)

                            changed = True

                            iter_info += 'M<->R containerM:' + str(containerM['orders']) + ' | containerR:' + str(containerR['orders'])

                            # if a swap is found, stop iterating the next order in containerR
                            break;
                
                if changed == True:
                    break;

            # if not all orders not put, continue
            if changed == True:
                break;
        
            find_cnt += 1

        if find_cnt >= find_limit:
            containersBlocked.append(containerM)
            solution.pop(0)
            continue

        if changed == True:
            # check the heap size
            num_containers = len(solution)

            # compute the average rate of the solution
            sum_rate = 0
            for container in solution:
                sum_rate += container['rate']
            avg_rate = sum_rate / num_containers

            # judge if the current solution is better
            if avg_rate > current_rate or (num_containers + len(containersBlocked)) < current_num_containers:
                # if the average utilization rate is higher than before
                # use the new solution
                current_rate = avg_rate
                current_num_containers = num_containers + len(containersBlocked)
                
                iter_info += ' | better score!'

                beat_best = True
                
            else:
                # changes are not more optimal, so return to the previous solution
                # but a random probability that the new solution is accepted
                delta = 10e16 * abs(current_rate - avg_rate)
                random_num = np.random.rand()
                if random_num < math.exp(-delta / temperature):
                    current_rate = avg_rate
                    current_num_containers = num_containers
                    iter_info += ' | not better, but acccepted.'
                else:
                    solution = solutionTemp.copy()

                    iter_info += ' | update fails.'
                
        else: 
            # worst case
            print('stuck!!!!!!!!!!!!!!!!!!!!!!!!!!!!! shit')

        temperature *= cooling_rate

        cur_res = len(solution) + len(containersBlocked)
        iter_info += f' | T={temperature: .1f} | Number: {cur_res}'

        if print_out:
            print(iter_info)

        with open(output_path, 'a') as file:
            file.write(iter_info + '\n')
    
        if temperature < 1: 
            break;

    best_total_num = len(solution) + len(containersBlocked)

    print(f'best number of containers: {best_total_num} | initial number of containers: {initial_num_containers}')

    for i in range(len(containersBlocked)):
        solution.append(containersBlocked[i])

    check_res = check.check(solution=solution, task=task)

    solution_file_name = 'result_' + task + '_SM_solution'
    solution_output.outputSolution(solution=solution, file_name=solution_file_name)

    print(check_res)

    return solution

def getContainerUtilizationRate(container):
    total_weight = sum(container['weights'])
    total_volume = sum(container['volumes'])
    total_pallets = sum(container['pallets'])

    utilization_rate = ((total_weight / 45000) + (total_volume / 3600) + (total_pallets / 60)) / 3

    # container['rate'].pop()
    container['rate'] = utilization_rate

    return utilization_rate

def getSolutionUtilizationRate(solution):
    return sum(container['rate'] for container in solution) / len(solution)

    

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

# check if an order can be added to a container (limit constraints)
def exceedLimit(cur_weight, cur_volume, cur_pallets, add_weight, add_volume, add_pallets):
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600
    return (cur_weight + add_weight > max_weight) or (cur_volume + add_volume > max_volume) or (cur_pallets + add_pallets > max_pallets)


def findBestRes(task, num_iter=100):
    
    current_best_solution = simulatedAnnealing(task=task, solution=None, num_iter=10000000000, print_out=False, initial_temperature=1000000000, cooling_rate=0.999)
    min_num_containers = len(current_best_solution)

    for i in range(num_iter):
        solution = simulatedAnnealing(task=task, solution=current_best_solution, num_iter=10000000000, print_out=False, initial_temperature=1000000000, cooling_rate=0.999)

        if check.check(solution=solution, task=task):
            if len(solution) < min_num_containers:
                current_best_solution = solution.copy()
                min_num_containers = len(solution)
                print(f'update better solution: {min_num_containers}')

                solution_output.outputSolution(solution=current_best_solution, file_name='result_' + task + '_SM_best_solution')

                # add iteration times
                num_iter += 100
            elif len(solution) == min_num_containers:
                print(f'not better, but update')
                current_best_solution = solution.copy()

        else:
            print('error occurs in the solution!')

    
    return

# findBestRes(task='a')