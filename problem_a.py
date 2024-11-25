from ortools.linear_solver import pywraplp
import read_data
import exact_search

def problemA(): 
    data = read_data.readData(task='a', first_n_rows=50, print_out=True)

    num_containers, output_message = exact_search.exactSearch(data=data, print_out=True)
    print("num_containers:", num_containers)

problemA();