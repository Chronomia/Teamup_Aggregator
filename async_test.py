import multiprocessing

def function1():
    print("Function 1")

def function2():
    print("Function 2")

def function3():
    print("Function 3")

def run_in_parallel():
    for _ in range(10):  # 10 iterations
        processes = [multiprocessing.Process(target=f) for f in [function1, function2, function3]]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

if __name__ == "__main__":
    run_in_parallel()
