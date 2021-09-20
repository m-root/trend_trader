from multiprocessing import Process

def loop_a(f):
    while 1:
        print(f)

# def loop_b():
#     while 1:
#         print("b")

if __name__ == '__main__':
    d = loop_a('a')
    c = loop_a('b')

    Process(target=d).start()
    Process(target=c).start()
    # Process(target=loop_b).start()