import exact_search
import read_data

def testLocalSize(task):

    complete_data = read_data.readData(task)
    size = len(complete_data['order number'])

    output_path = './output/result_a_local_size_test.txt'

    with open(output_path, 'w') as file:
        file.write("")
    
    for i in range(1, size):
        data = read_data.readShuffledData(task, first_n_rows=i)

        res, _ = exact_search.exactSearch(data=data, print_out=False)
        message = 'Test data with ' + str(i) +' rows: ' + str(res) + ' containers' + '\n'
        # print and write the message
        print(message)
        with open(output_path, 'a') as file:
            file.write(message)
    
    
testLocalSize(task='a')
