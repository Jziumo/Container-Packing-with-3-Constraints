from ortools.linear_solver import pywraplp
import read_data

def main():
    # @注意：可以尝试添加第2个参数，表示只计算前n个订单的结果 
    data = read_data.readSortedData('a', sort_by='weight', ascending=True, first_n_rows=None)
    # data = read_data.readSortedData('a', sort_by='weight', ascending=True, first_n_rows=40)
    # data = read_data.readData('a')

    size = len(data['order number'])
    # print(size)
    
    max_pallets = 60
    max_weight = 45000
    max_volume = 3600

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

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
    
    # start solving
    print(f"Solving with {solver.SolverVersion()}")
    with open('./output/result_a.txt', "w") as file: 
        file.write(f"Solving with {solver.SolverVersion()}\n")
    status = solver.Solve()

    # result string
    output_message = ""

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
                output_message += f"- Orders packed: {container_items}\n"
                output_message += f"- Weight: {container_weight}\n"
                output_message += f"- Volume: {container_volume}\n"
                output_message += f"- Pallets: {container_pallets}\n"
                
                # check if the container satisfies the capacity constraint
                satisfy_contraint = True
                if container_weight <= max_weight and container_volume <= max_volume and container_pallets <= max_pallets:
                    output_message += "(satisfies the capacity constraints)\n"
                else: 
                    output_message += "container is overloaded!\n"
                    satisfy_contraint = False
                    all_satisfied = False

                # if satisfy the constraint, then analyze the utilization rate
                if satisfy_contraint:
                    utilization_rate = (container_weight / max_weight + container_volume / max_volume + container_pallets / max_pallets) / 3
                    rates.append(utilization_rate)
                    output_message += f"Average utilization rate of the container: {utilization_rate}\n"

                output_message += "\n"
                num_containers += 1

        output_message += "Total analysis: \n"

        # calculate the total amount 
        total_weight = sum(weights)
        total_volume = sum(volumes)
        total_pallets = sum(pallets)
        
        # calculate the utilization rate of each column
        weight_rate = total_weight / (max_weight * num_containers)
        volume_rate = total_volume / (max_volume * num_containers)
        pallets_rate = total_pallets / (max_pallets * num_containers)

        output_message += "|- Utilization rate"
        # 写到一半你就要看代码😡 


        output_message += f"Total number of containers used: {num_containers}\n"

        # output if all the containers satisfy the capacity constraint
        if all_satisfied: 
            output_message += "All containers satisfy the capacity constraints.\n"
        else: 
            output_message += "Some containers are overloaded!\n"

        print(output_message) 

    else: 
        # the problem is not solved for some reason
        output_message += f"The problem is not solved. The status is {status}\n"

    # write the result to the file
    with open("output/result_a.txt", "a") as file: 
        file.write(output_message)    

if __name__=="__main__":
    main()