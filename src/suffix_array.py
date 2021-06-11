import subprocess, os
from tally import fast_rank


def sais_suffix_array(file: str):
    """ 
    Using sais algorithm to generate suffix array 
    :param file: path to file
    """
    temp_out_file = 'sa_output.txt'
    subprocess.call([f'{os.path.dirname(__file__)}\\sais\\sais.exe', file, temp_out_file], stderr=subprocess.DEVNULL)
    with open(temp_out_file, 'r') as file:
        data = file.read()
    os.remove(temp_out_file)
    array = [int(i) for i in data.split(' ')]
    return array


def generate_suffix_array(T: str, sa_factor: int = 1, array = None):    
    """
    Generate suffix array with sa factor, function can use pre-calculated suffix array 
    to reduce execution time and space consumption
    :param file: path to file
    :param sa_factor:
    :param array: pre-calculated suffix array
    """
    if array is None:
        with open('tmp_file.txt', 'w') as file:
            file.write(T)
        array = sais_suffix_array('tmp_file.txt')
        os.remove('tmp_file.txt')

    suffix_array = {}

    for i in range(len(array)):
        if not(array[i] % sa_factor):
            suffix_array.update({i : array[i]})
        
    return suffix_array


def resolve_fm_index_offset(suffix_array, row, L, F, tally, tally_factor=1):
    step_cnt = 0
    
    while True:
        
        if row in suffix_array:
            break

        char = L[row]
        rank = fast_rank(tally, row, char, L, tally_factor) - 1
        row = F[char] + rank
        step_cnt += 1
    
    return suffix_array[row] + step_cnt
