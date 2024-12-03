
from ortools.linear_solver import pywraplp
import read_data
import greedy_solution as greedy

def exactSearch(task, data, print_out=True, solver_type="SCIP", greedy_hint=True):

    size = len(data['order number'])
    # print(size)
    
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver(solver_type)
    # solver.set_time_limit(10000)

    if not solver:
        return

    # Decision Variables
    # x[i, j] = 1 if order i is packed in container j.
    x = {}
    for i in range(size): 
        for j in range(size): 
            x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" % (i, j))

    # y[j] = 1 if container j is used.
    y = {}
    for j in range(size): 
        y[j] = solver.IntVar(0, 1, "y[%i]" % j)

    # Constraints
    # Constraints: Capacity constraint
    # iterate each container j
    for j in range(size): 
        solver.Add(sum(x[(i, j)] * data['weight'][i] for i in range(size)) <= y[j] * max_weight)
        solver.Add(sum(x[(i, j)] * data['pallets'][i] for i in range(size)) <= y[j] * max_pallets)
        solver.Add(sum(x[(i, j)] * data['volume'][i] for i in range(size)) <= y[j] * max_volume)

    # Constraints: Each item must be in exactly one container
    # iterate each order i
    for i in range(size): 
        solver.Add(sum(x[(i, j)] for j in range(size)) == 1)
        
    # Objective: minimize the number of containers used.
    solver.Minimize(solver.Sum([y[j] for j in range(size)]))

    if greedy_hint:
        variables = []
        hint_values = []

        x_initial, y_initial = generateInitialSolution(task=task, problem_used_data=data)

        containers_cnt = 0
        for j in range(size):
            if y_initial[j] == 1:
                containers_cnt += 1

        if print_out:
            print("Initial solution given by greedy method:", containers_cnt)

        for i in range(size):
            for j in range(size):
                variables.append(x[(i, j)])
                hint_values.append(x_initial[i][j])
        for j in range(size):
            variables.append(y[j])
            hint_values.append(y_initial[j])

        solver.SetHint(variables, hint_values)
    
    # start solving
    if print_out:
        print(f"Solving with {solver.SolverVersion()}")
    with open('./output/result_a.txt', "w") as file: 
        file.write(f"Solving with {solver.SolverVersion()}\n")
    status = solver.Solve()

    # result string
    output_message = ""
    num_containers = -1

    if status == pywraplp.Solver.OPTIMAL:
        # if the problem is solved
        # print the result and analyze the solutions
        num_containers = 0

        # variables used to calculate the utilization rate
        weights = []
        volumes = []
        pallets = []
        rates = []

        # check if all the containers satisfy the capacity constraint
        all_satisfied = True

        # iterate each container
        for j in range(size): 
            # if this container is used
            if y[j].solution_value() == 1:
                container_items = []
                container_weight = 0
                container_volume = 0
                container_pallets = 0

                for i in range(size): 
                    # iterate each item in this container
                    if x[(i, j)].solution_value() == 1:
                        container_items.append(data['order number'][i])
                        container_weight += data['weight'][i]
                        container_volume += data['volume'][i]
                        container_pallets += data['pallets'][i]

                # record the weightss, volumes, and pallets
                weights.append(container_weight)
                volumes.append(container_volume)
                pallets.append(container_pallets)

                output_message += f"Container {j}:\n" 
                output_message += f"├─ Orders packed: {container_items}\n"
                output_message += f"├─ Weight: {container_weight}\n"
                output_message += f"├─ Volume: {container_volume}\n"
                output_message += f"├─ Pallets: {container_pallets}\n"
                
                # check if the container satisfies the capacity constraint
                satisfy_contraint = True
                if container_weight <= max_weight and container_volume <= max_volume and container_pallets <= max_pallets:
                    output_message += "├─ (satisfies the capacity constraints)\n"
                else: 
                    output_message += "├─ container is overloaded!\n"
                    satisfy_contraint = False
                    all_satisfied = False

                # if satisfy the constraint, then analyze the utilization rate
                if satisfy_contraint:
                    utilization_rate = (container_weight / max_weight + container_volume / max_volume + container_pallets / max_pallets) / 3
                    rates.append(utilization_rate)
                    output_message += f"└─ Average utilization rate of the container: {utilization_rate: .4f}\n"

                output_message += "\n"
                num_containers += 1

        output_message += "Total analysis: \n"

        output_message += f"├─ Total number of containers used: {num_containers}\n"

        # calculate the total amount 
        total_weight = sum(weights)
        total_volume = sum(volumes)
        total_pallets = sum(pallets)
        
        # calculate the utilization rate of each column
        weight_rate = total_weight / (max_weight * num_containers)
        volume_rate = total_volume / (max_volume * num_containers)
        pallets_rate = total_pallets / (max_pallets * num_containers)
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

        if print_out:
            print(output_message) 

    else: 
        # the problem is not solved for some reason
        output_message += f"The problem is not solved. The status is {status}\n"

    # write the result to the file
    with open("output/result_a.txt", "a") as file: 
        file.write(output_message)    

    return num_containers, output_message

def generateInitialSolution(task, problem_used_data):
    # use greedy method to generate an intial solution
    df = read_data.getDataFrame(task)
    df['lambda'] = greedy.getOrderLambda(df, y=100)
    data = read_data.getMap(read_data.sort(df, sort_by='lambda', ascending=False))
    solution, num_containers = greedy.greedy(task=task, data=data, print_out=False)

    # because the data used by greedy method is sorted, it cannot be used to find the indices of orders
    data = problem_used_data
    
    # print(num_containers)
    size = len(data['order number'])

    # x[i, j] = 1 if order i is packed in container j.
    # y[j] = 1 if container j is used.
    x_initial = [[0] * size] * size
    y_initial = [0] * size

    for i in range(num_containers):
        container = solution[i]
        num_orders = len(container['orders'])
        container_idx = getOrderIndex(data, container['orders'][0])
        y_initial[container_idx] = 1

        for j in range(num_orders):
            order_idx = getOrderIndex(data, container['orders'][j])
            x_initial[order_idx][container_idx] = 1

    return x_initial, y_initial

def getOrderIndex(data, order_number):
    for i in range(len(data['order number'])):
        if data['order number'][i] == order_number:
            return i
    return -1


# generateInitialSolution(task='a')