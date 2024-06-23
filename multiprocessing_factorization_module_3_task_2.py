from time import time
from multiprocessing import Pool, cpu_count


def time_counter(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        finish_time = time()
        print(f"The task took {finish_time - start_time:.4f} seconds")
        return result
    return wrapper


"""synchronous solution"""


@time_counter
def factorize(*number):
    final_result = []
    for num in number:
        result_for_number = []
        for i in range(1, num+1):
            if num % i == 0:
                result_for_number.append(i)
        final_result.append(result_for_number)
    return final_result


"""multiprocessing solution"""


def factorize_one_number(num):
    result_one_number = []
    for i in range(1, num + 1):
        if num % i == 0:
            result_one_number.append(i)
    return result_one_number


@time_counter
def factorize_numbers(*number):
    with Pool(cpu_count()) as pool:
        result_all_numbers = pool.map(factorize_one_number, number)
    return result_all_numbers


def main():
    # Synchronous solution
    print("Synchronous solution:")
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    # Multiprocessing solution
    print("Multiprocessing solution:")
    e, f, g, h = factorize_numbers(128, 255, 99999, 10651060)
    assert e == [1, 2, 4, 8, 16, 32, 64, 128]
    assert f == [1, 3, 5, 15, 17, 51, 85, 255]
    assert g == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert h == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    print(f"CPU count: {cpu_count()}")


if __name__ == '__main__':
    main()
