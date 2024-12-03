from ortools.linear_solver import pywraplp
import read_data
import exact_search

def problemA(): 
    data = read_data.readData(task='a', first_n_rows=100, print_out=True)

    num_containers, output_message = exact_search.exactSearch(task='a', data=data, print_out=True, greedy_hint=True)
    print("num_containers:", num_containers)

problemA()