import time
import atexit

def test_time():
    start = time.time()
    for i in range(100000):
        assert i + 1 > 0
    end = time.time()
    print(end - start)

def goodbye(name, adjective):
    print(f"Goodbye {name}, it was {adjective} to meet you.")

if __name__ == '__main__':
    atexit.register(goodbye, adjective='nice', name='Donny')
    for i in range(100000000):
        if i % 10000000 == 0:
            print(i)
