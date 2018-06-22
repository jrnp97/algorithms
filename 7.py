import time


def is_prime(num):
    for i in list(range(2, num)):
        if num % i == 0:
            return False
    return True


if __name__ == "__main__":
    start = time.perf_counter()
    count = 1
    number = 1
    while count <= 10002:
        if is_prime(number):
            count += 1
        number += 1
    end = time.perf_counter()
    print(f"Solution {number - 1} in {(end-start)/60} minutes")
