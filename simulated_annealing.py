import read_data
import greedy_solution as greedy
import find_neighborhood as fn
import check

def simulatedAnnealing(task):
    # use greedy method to generate an intial solution
    df = read_data.getDataFrame(task)
    df['lambda'] = greedy.getOrderLambda(df, y=100)
    data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))
    initial_solution, num_containers = greedy.greedy(task, data=data, print_out=False)
    
    # record the best solution
    best_solution = initial_solution
    best_num_containers = num_containers
    current_solution = initial_solution

    num_iterations = 10000
    for i in range(num_iterations):
        current_solution,_ = fn.randomMoveOrders(solution=current_solution)

        # remove the empty containers
        current_solution = [container for container in current_solution if len(container['orders']) > 0]

        current_num_containers = len(current_solution)
        if current_num_containers < best_num_containers:
            best_solution = current_solution
            best_num_containers = current_num_containers

    check_res = check.check(solution=best_solution)

    print("best number of containers:", best_num_containers)
    print(check_res)
    return best_solution

simulatedAnnealing(task='a')