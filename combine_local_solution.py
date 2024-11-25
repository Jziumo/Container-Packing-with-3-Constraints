import read_data
import exact_search

def combineLocalSolution(task, batch_capacity=95):
    df = read_data.shuffle(read_data.getDataFrame(task))
    size = df.shape[0]
    
    start = 0
    end = batch_capacity
    total_num_containers = 0

    while start < size:
        batch = read_data.getMap(read_data.extract(df, start, end))

        batch_size = len(batch['order number']);

        num_containers, _ = exact_search.exactSearch(data=batch, print_out=False)

        print('start:', start, '| end:', end,'| batch size:', batch_size, '| number of containers:', num_containers)

        total_num_containers += num_containers

        # update indices
        start = end
        end = start + batch_capacity
        
        if end > size: 
            end = size

    print('Total number of containers:', total_num_containers)


combineLocalSolution('a', batch_capacity=20)