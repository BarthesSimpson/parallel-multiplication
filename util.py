def add(*args):
    """
    Adds an arbitrary number of numbers represented 
    as arrays by using primitive addition at each
    cardinality and carrying to the left
    when a slot overflows.

    :param args: *[]int
    :rtype []int
    """
    padded = match_padding(*args)
    x = padded[0]
    res = [0] * len(x)
    for i in range(len(x)):
        index = len(x) - (1 + i)
        res[index] += sum([num[index] for num in padded])
        res = carry_left(res, i)
    return res


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


def match_padding(*args):
    """
    Pads numbers with leading zeros until 
    all numbers have matching length
    :param args: *[]int
    :rtype *[]int
    """
    max_length = len(args[0])
    for num in args[1:]:
        length = len(num)
        if length > max_length:
            max_length = length
    return [pad(num, max_length - len(num)) for num in args]


def pad(num, padding, side='left'):
    """
    Pads a number expressed as an array with leading zeros
    or trailing zeros if side is specified as 'right'
    :param num: []int
    :param padding: int
    :rtype []int
    """
    return [*num,
            *([0] * padding)] if side is 'right' else [*([0] * padding), *num]


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


def split(num):
    """
    Given a number expressed as an array of digits, split
    at the midpoint and return each half. For odd length
    number, the upper half will contain the extra digit.    
    :param num: []int
    :rtype: []int []int
    """
    mid = len(num) // 2
    return num[:mid], num[mid:]


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


def subtract(x, y):
    """
    Subtracts a number y from another number x where
    both numbers are represented as arrays. Assumes
    the numbers have been pre-padding with leading 
    zeros so as to be of equal length. x must be 
    larger than y - no negative numbers here I'm
    afraid.

    :param x: []int
    :param y: []int
    :rtype []int
    """
    res = [0] * len(x)
    # go from left to right, subtracting
    # pairwise
    for i in range(len(x)):
        sub = x[i] - y[i]
        # if we went negative, 'carry' the
        # negative ten to the left and leave
        # the remainder in this slot
        if sub < 0:
            res[i] = 10 + sub
            res[i - 1] -= 1
        # otherwise, just put the result of
        # the pairwise subtraction in the
        # current slot
        else:
            res[i] = sub
    return res


if __name__ == '__main__':

    print('testing add')
    assert add([0], [0]) == [0]
    assert add([1], [0]) == [1]
    assert add([1], [1]) == [2]
    assert add([2], [3]) == [5]
    assert add([2, 0], [3, 0]) == [5, 0]
    assert add([8, 4], [3, 5]) == [1, 1, 9]
    assert add([2, 4, 5], [0, 6, 7]) == [3, 1, 2]
    assert add([2, 4, 5], [0, 6, 7], [0, 0, 5]) == [3, 1, 7]
    assert add([6, 0, 0], [0], [0, 0]) == [6, 0, 0]

    print('testing match_padding')
    assert match_padding([6, 0, 0], [0], [0, 0]) == [[6, 0, 0], [0, 0, 0],
                                                     [0, 0, 0]]
    assert match_padding([0, 0], [6, 0, 0], [0]) == [[0, 0, 0], [6, 0, 0],
                                                     [0, 0, 0]]

    print('testing carry_left')
    assert carry_left([0, 20], 0) == [2, 0]
    assert carry_left([0, 24], 0) == [2, 4]
    assert carry_left([11, 9], 1) == [1, 1, 9]

    print('testing pad')
    assert pad([1], 0) == [1]
    assert pad([1], 1) == [0, 1]
    assert pad([], 1) == [0]
    assert pad([], 1, 'right') == [0]
    assert pad([1], 1, 'right') == [1, 0]

    print('testing subtract')
    assert subtract([0], [0]) == [0]
    assert subtract([1], [0]) == [1]
    assert subtract([1], [1]) == [0]
    assert subtract([5], [2]) == [3]
    assert subtract([5, 0], [3, 0]) == [2, 0]
    assert subtract([8, 4], [3, 5]) == [4, 9]
    assert subtract([2, 4, 5], [0, 6, 7]) == [1, 7, 8]
