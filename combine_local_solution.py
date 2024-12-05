import read_data
import exact_search

def combineLocalSolution(task, batch_size_approximate=76):
    
    batches = read_data.getSortedDataBatches(task=task, w=1, v=1, p=1, batch_size_approximate=batch_size_approximate, ascending=True, print_out=True)
    
    num_batches = len(batches)
    total_num_containers = 0

    for i in range(num_batches):
        batch = batches[i]
        
        num_containers, _ = exact_search.exactSearch(task=task, data=batch, print_out=False, greedy_hint=False)

        print(f'batch {i}: number of containers = {num_containers}')

        total_num_containers += num_containers

    print('Total number of containers:', total_num_containers)


combineLocalSolution('a', batch_size_approximate=76)