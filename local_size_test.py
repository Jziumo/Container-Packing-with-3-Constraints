import exact_search
import read_data

def testSizeLimit(task):

    complete_data = read_data.readData(task)
    size = len(complete_data['order number'])

    output_path = './output/result_' + task + '_size_limit.txt'

    with open(output_path, 'w') as file:
        file.write("")
    
    for i in range(1, size):
        data = read_data.readSortedData(task=task, w=1, v=201, p=1, first_n_rows=i)

        res, _ = exact_search.exactSearch(task=task, data=data, print_out=False, greedy_hint=False)
        message = 'Test data with ' + str(i) +' rows: ' + str(res) + ' containers' + '\n'
        # print and write the message
        print(message)
        with open(output_path, 'a') as file:
            file.write(message)
    return
    
def testSize(task, size, w=1, v=1, p=1, ascending=False):
    data = read_data.readSortedData(task=task, w=w, v=v, p=p, ascending=ascending, first_n_rows=size)

    output_path = './output/result_' + task + '_size_test.txt'

    with open(output_path, 'w') as file:
        file.write("")
    
    res, _ = exact_search.exactSearch(task=task, data=data, print_out=True, greedy_hint=False)

    message = 'Test data with ' + str(size) +' rows: ' + str(res) + ' containers' + '\n'
    # print and write the message
    print(message)
    with open(output_path, 'a') as file:
        file.write(message)

    return

def testDataPart():
    # @todo
    data = read_data.readSortedData(task='a', sort_by='weight', ascending=False, first_n_rows=100)

    res, _ = exact_search.exactSearch(task='a', data=data, print_out=False, greedy_hint=True)

    print(res)

    return

# testSizeLimit('a')
testSize('a', 101, w=1, v=201, p=1, ascending=True)