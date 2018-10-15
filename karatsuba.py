"""
This module implements integer multiplication
using a recursive implementation of the Karatsuba 
algorithm, falling back to the grade school 
algorithm for the base case. The 
algorithm has O(n*log n) time complexity and 
O(n) space complexity.
"""

from util import add, carry_left, match_padding, pad, split, subtract
from grade_school import multiply_simple


def multiply_karatsuba(x, y):
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
    # print(x, y)

    if len(x) == 1:
        return multiply_simple(x, y)

    res_1 = multiply_karatsuba(a, c)
    res_2 = multiply_karatsuba(b, d)
    # print('ha')
    # print(a)
    # print(b)
    # print(add(a, b))
    # print('ho')

    partial = multiply_karatsuba(add(a, b), add(c, d))
    # res_3 is partial - res_1 - res_2.
    # To simplify, just add res_1 and res_2 then subtract that sum from partial
    res_3 = subtract(partial, add(res_1, res_2))
    # print(pad(res_1, len(x), 'right'), res_2, pad(res_3,
    #                                             len(x) // 2, 'right'))
    res = add(
        pad(res_1, len(x), 'right'), res_2, pad(res_3,
                                                len(x) // 2, 'right'))

    return res


if __name__ == '__main__':

    print('testing karatsuba')
    assert multiply_karatsuba([0], [0]) == [0]
    assert multiply_karatsuba([1], [0]) == [0]
    assert multiply_karatsuba([1], [1]) == [1]
    assert multiply_karatsuba([2], [3]) == [6]
    assert multiply_karatsuba([2, 0], [3, 0]) == [6, 0, 0]
    # assert multiply_karatsuba([2, 4], [3, 5]) == [8, 4, 0]
    # assert multiply_karatsuba([2, 4, 5], [6, 7]) == [1, 6, 4, 1, 5]

    # import time
    # start = time.time()
    # multiply_karatsuba([
    #     6, 5, 4, 3, 2, 1, 2, 4, 5, 6, 7, 8, 9, 2, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5,
    #     4, 3, 2, 1
    # ], [
    #     6, 5, 4, 3, 2, 1, 2, 4, 5, 6, 7, 8, 9, 2, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5,
    #     4, 3, 2, 1
    # ])
    # end = time.time()
    # print((end - start) * 1000)
    # print(
    #     len([
    #         6, 5, 4, 3, 2, 1, 2, 4, 5, 6, 7, 8, 9, 2, 4, 5, 6, 7, 8, 9, 8, 7,
    #         6, 5, 4, 3, 2, 1
    #     ]))
    # start = time.time()
    # 6543212456789245678987654321245678987654321 * 6543212456789245678987654321245678987654321
    # end = time.time()
    # print((end - start) * 1000)
