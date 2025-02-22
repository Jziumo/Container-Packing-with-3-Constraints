from ortools.linear_solver import pywraplp
import read_data
import exact_search
import solution_input
import solution_output
import greedy_solution as greedy
import simulated_annealing as sm
import check

def problemC(): 

    # solution = solution_input.inputSolution(task='c', file_name='c_sm', print_out=False)
    
    current_best_solution = sm.simulatedAnnealing(task='c', solution=None)
    min_num_containers = len(current_best_solution)

    iter_num = 1000
    iter_cnt = 0
    while iter_cnt < iter_num:
        solution = sm.simulatedAnnealing(task='c', solution=current_best_solution, num_iter=10000000000000, print_out=False, order_repeat_limit=60, initial_temperature=1000000000, cooling_rate=0.999, epsilon=10e20)

        if check.check(solution=solution, task='c'):
            if len(solution) < min_num_containers:
                current_best_solution = solution.copy()
                min_num_containers = len(solution)
                print(f'update better solution: {min_num_containers}')

                solution_output.outputSolution(solution=current_best_solution, file_name='result_a_SM_best_solution')

                # add iteration times
                iter_num += 100
            elif len(solution) == min_num_containers:
                print(f'not better, but update')
                current_best_solution = solution.copy()

        else:
            print('error occurs in the solution!')

        iter_cnt += 1

problemC() 