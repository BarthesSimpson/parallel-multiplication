"""
This module implements integer multiplication
using only the primitive of addition. The 
algorithm has O(n^2) time complexity and 
O(n) space complexity.
"""


def multiply_simple(x, y):
    """
    Multiplies two numbers represented as arrays
    using the grade school algorithm of cross-multiplying
    each pair of digits and "carrying" to the left when
    a pairwise multiplication results in a number larger
    than 9.

    :param x: []int
    :param y: []int
    :rtype []int
    """
    # Pad the shorter number with leading zeros
    if len(x) > len(y):
        y = pad(y, len(x) - len(y))

    if len(y) > len(x):
        x = pad(x, len(y) - len(x))

    # Create a new list for the result
    res = [0] * len(x)

    # iterate from right to left, "multiplying"
    # the digit from x and the digit from y
    # by adding them and putting them into the
    # correct slot, carrying whenever the value
    # for that slot exceeds 9
    for i in range(len(x)):
        for j in range(len(y)):
            # figure out which slot we should be
            # adding our numbers to
            cardinality = i + j
            # get our pair for pairwise multiplication
            a = x[len(x) - (i + 1)]
            b = y[len(y) - (j + 1)]
            # if either of the numbers to be pairwise multiplied is zero,
            # we can just skip ahead; otherwise, "multiply" the pair
            if a > 0 and b > 0:
                for _ in range(a):
                    # first, need to make sure there is a slot to the left;
                    # if not, create it by adding more left padding
                    res = pad_if_needed(res, cardinality)
                    res[len(res) - (cardinality + 1)] += b
                # if the number overflowed, carry to the left recursively
                res = carry_left(res, cardinality)

    return strip_leading_zeros(res)


def carry_left(num, cardinality):
    """
    Carries an overflowing digit to the left,
    starting at the digit located at num[cardinality]
    and repeating leftwards until all digits are
    below 9. Returns the num list with the carries
    applied.

    :param num: []int
    :param cardinality: int
    :rtype []int
    """
    digit = num[len(num) - (cardinality + 1)]
    while digit > 9:
        # first, need to make sure there is a slot to the left;
        # if not, create it by adding more left padding
        num = pad_if_needed(num, cardinality)
        # now, grab the next slot to the left and
        # start dumping tens into it
        digit -= 10
        num[len(num) - (cardinality + 1)] = digit
        num[len(num) - (cardinality + 2)] += 1
        # if we got below 10, move one place to the left
        # and carry on (see what I did there?)
        if digit < 10:
            cardinality += 1
            digit = num[len(num) - (cardinality + 1)]

    return num


def pad(num, padding):
    """
    Pads a number expressed as an array with leading zeros
    :param num: []int
    :param padding: int
    :rtype []int
    """
    return [*([0] * padding), *num]


def pad_if_needed(num, cardinality):
    """
    Given that we will be increasing a digit of the given cardinality,
    Add leading zeros if that slot has not yet been created
    :param num: []int
    :param cardinality: int
    :rtype: []int
    """
    if len(num) < (cardinality + 2):
        num = pad(num, (cardinality + 2) - len(num))
    return num


def strip_leading_zeros(num):
    """
    In case we padded but didn't need it,
    remove the excess zeros.
    :param num: []int
    :rtype: []int
    """
    # for empty list, just return 0
    if len(num) == 0:
        return [0]
    # for non-empty list, strip the zeros;
    i = 0
    while i < len(num) and num[i] == 0:
        i += 1
    stripped = num[i:]
    # if every digit was zero, return 0
    return stripped if len(stripped) > 0 else [0]


if __name__ == '__main__':

    print('testing pad')
    assert pad([1], 0) == [1]
    assert pad([1], 1) == [0, 1]
    assert pad([], 1) == [0]

    print('testing carry_left')
    assert carry_left([0, 20], 0) == [2, 0]
    assert carry_left([0, 24], 0) == [2, 4]

    print('testing multiply_simple')
    assert multiply_simple([0], [0]) == [0]
    assert multiply_simple([1], [0]) == [0]
    assert multiply_simple([1], [1]) == [1]
    assert multiply_simple([2], [3]) == [6]
    assert multiply_simple([2, 0], [3, 0]) == [6, 0, 0]
    assert multiply_simple([2, 4], [3, 5]) == [8, 4, 0]
    assert multiply_simple([2, 4, 5], [6, 7]) == [1, 6, 4, 1, 5]
