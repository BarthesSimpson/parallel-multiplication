"""
This module implements integer multiplication
using a recursive implementation of the Karatsuba 
algorithm, falling back to the grade school 
algorithm for the base case. It implements some 
parallelization using multiprocessing. The 
algorithm has O(n*log n) time complexity and 
O(n) space complexity.

Currently, it gets the wrong answer, but at least
it is a deterministically wrong answer...
"""

from multiprocessing import Manager, Process
import random

from util import add, carry_left, match_padding, pad, split, subtract
from grade_school import multiply_simple
from big_numbers import big_number, big_number_as_array, big_res

# global manager and thread-safe container for partial results
manager = Manager()
return_dict = manager.dict()


def multiply_karatsuba_parallel(x, y, key=None):
    """
    Multiplies two numbers represented as arrays
    using the Karatsuba algorithm, falling back
    on grade school algorithm for the base case

    :param x: []int
    :param y: []int
    :rtype []int
    """
    x, y = match_padding(x, y)
    a, b = split(x)
    c, d = split(y)

    # for base case, go simple
    if len(x) == 1:
        return multiply_simple(x, y)

    # for big numbers, go parallel
    if len(x) > 300:
        # generate random ids for the subprocess outputs
        r1 = random.random()
        r2 = random.random()
        r3 = random.random()

        # run the sub-multiplications in parallel
        p1 = Process(target=multiply_karatsuba_parallel, args=[a, c, r1])
        p2 = Process(target=multiply_karatsuba_parallel, args=[b, d, r2])
        p3 = Process(
            target=multiply_karatsuba_parallel,
            args=[add(a, b), add(c, d), r3])

        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()

        # get the results
        res_1 = return_dict[r1]
        res_2 = return_dict[r2]
        partial = return_dict[r3]

    # for smaller numbers, don't bother parallelizing
    else:
        res_1 = multiply_karatsuba_parallel(a, c)
        res_2 = multiply_karatsuba_parallel(b, d)
        partial = multiply_karatsuba_parallel(add(a, b), add(c, d))

    # do the karatsuba shuffle
    res_3 = subtract(partial, add(res_1, res_2))
    res = add(
        pad(res_1, len(x), 'right'), res_2,
        pad(res_3, (len(x) + 1) // 2, 'right'))

    # if we are in parallel mode, write the result to the global dict
    if key is not None:
        return_dict[key] = res

    return res


if __name__ == '__main__':

    assert multiply_karatsuba_parallel([2, 4, 5], [6, 7]) == [1, 6, 4, 1, 5]
    print(
        multiply_karatsuba_parallel(big_number_as_array, big_number_as_array))
    assert multiply_karatsuba_parallel(big_number_as_array,
                                       big_number_as_array) == big_res

    import time
    start = time.time()
    multiply_karatsuba_parallel(big_number_as_array, big_number_as_array)
    end = time.time()
    print('karatsuba', (end - start) * 1000, 'milliseconds')
    start = time.time()
    big_number * big_number
    end = time.time()
    print('native', (end - start) * 1000, 'milliseconds')
