import numpy as np
import math
import read_data
import greedy_solution as greedy
import find_neighborhood as fn
import check

def simulatedAnnealing(task, cooling_rate=0.98, initial_temperature=100000000, num_iterations=10000):
    # use greedy method to generate an intial solution
    df = read_data.getDataFrame(task)
    df['lambda'] = greedy.getOrderLambda(df, y=100)
    data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))
    initial_solution, num_containers = greedy.greedy(task, data=data, print_out=False)
    
    # record the best solution
    best_solution = initial_solution
    best_score = evaluate(best_solution)
    current_solution = initial_solution
    current_score = evaluate(current_solution)
    temperature = initial_temperature

    # num_iterations = 10000
    for i in range(num_iterations):
        # generate a neighbor solution
        # current_solution, changed = fn.randomMoveOrders(solution=current_solution)
        neighbor_solution, changed = fn.randomSwapOrders(solution=current_solution, penalty_allowed=True)

        # remove the empty containers
        neighbor_solution = [container for container in current_solution if len(container['orders']) > 0]
        number_containers = len(neighbor_solution)

        # evaluate the score of the neighbor solution
        neighbor_score = evaluate(neighbor_solution)

        changed = False
        
        if neighbor_score < current_score:
            current_solution = neighbor_solution
            current_score = neighbor_score

            changed = True

            if current_score < best_score:
                best_solution = current_solution
        else:
            delta = neighbor_score - current_score
            random_num = np.random.rand()
            if random_num < math.exp(-delta / temperature):
                current_solution = neighbor_solution
                current_score = neighbor_score
                
                changed = True

        print("neighbor score:", neighbor_score, "| temperature:", temperature, "| num containers:", number_containers, "|", changed)

        temperature *= cooling_rate
        
        if temperature < 1: 
            break;

    check_res = check.check(solution=best_solution)
    print(check_res)
    return best_solution

# return the score of the solution
def evaluate(solution, alpha=10, beta=10, gamma=10, mu=10): 
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    weight_penalty = 0
    volume_penalty = 0
    pallets_penalty = 0

    # iterate each containers
    num_containers = len(solution)
    for i in range(num_containers):
        container = solution[i]

        container_weight = sum(container['weights'])
        container_volume = sum(container['volumes'])
        container_pallets = sum(container['pallets'])
        
        weight_penalty += max(0, container_weight - max_weight)
        volume_penalty += max(0, container_volume - max_volume)
        pallets_penalty += max(0, container_pallets - max_pallets)

    score = alpha * weight_penalty + beta * volume_penalty + gamma * pallets_penalty
    return score

simulatedAnnealing(task='a')