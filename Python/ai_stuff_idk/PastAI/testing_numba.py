import time

def check_for_evens(array):
    return_array = []
    for element in array:
        if element % 2 == 0:
            return_array.append(0)
        else:
            return_array.append(1)
    return return_array

if __name__ == "__main__":
    sample_array = list(range(10000000))
    
    start_time = time.time()
    result = check_for_evens(sample_array)
    print(f"Execution time: {time.time() - start_time:0.6f} seconds")