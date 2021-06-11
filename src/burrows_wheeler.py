import os
from suffix_array import sais_suffix_array


MARKER = '$'


def burrows_wheeler_transform(T: str, array = None) -> str:
    """
    BWT can use pre-calculated suffix array to reduce execution time and space consumption
    :param T: string
    :param array: pre-calculated suffix array
    :return: BWT
    """
    if array is None:
        with open('tmp_file.txt', 'w') as file:
            file.write(T)
        array = sais_suffix_array('tmp_file.txt')
        os.remove('tmp_file.txt')

    bwt = []
    
    for index in array:
        if index == 0:
            bwt.append(MARKER)
        else:
            bwt.append(T[index - 1])
    
    return ''.join(bwt)


def first_column(L: str):
    """ Returns first column of BWT in format: 'char : start_index' """
    chars = sorted(set(L))
    chars.remove(MARKER)
    
    chars_cnt = dict(zip(iter(chars), [0]*len(chars)))
  
    for char in L:
        if char != MARKER:
            chars_cnt[char] += 1

    first_col = {chars[0] : 1}
    
    prev_c = chars[0]
    for char in chars[1:]:
        first_col[char] = first_col[prev_c] + chars_cnt[prev_c]
        prev_c = char

    return first_col
