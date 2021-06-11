from Bio import SeqIO
from burrows_wheeler import MARKER, burrows_wheeler_transform, first_column
from tally import fast_rank, generate_tally
from suffix_array import generate_suffix_array, resolve_fm_index_offset, sais_suffix_array


def load_file(file_path: str):
    fasta_sequences = SeqIO.parse(open(file_path),'fasta')
    sequence = ""
    for fasta in fasta_sequences:
        sequence += str(fasta.seq)
    return sequence


def prepare_file(data: str):
    temp_file = 'genom_with_marker.txt'
    with open(temp_file, 'w') as file:
        file.write(data)
    return temp_file


def search_benchmark(pattern, F, L, SA, tally, tally_factor):
    """ Search algorithm adopted for benchmarking of seraching results """
    match = []

    first_column_chars = list(F)
    last_char_in_pattern_index = first_column_chars.index(pattern[-1])

    char_first_index = F[pattern[-1]] 
    if last_char_in_pattern_index < len(F) - 1:
        char_last_index = F[first_column_chars[last_char_in_pattern_index + 1]] - 1 
    else:
        char_last_index = len(L) - 1

    for pattern_index in range(len(pattern) - 1, -1, -1):
        if pattern_index > 0:
            char = pattern[pattern_index - 1]
            
            tally_min = fast_rank(tally, char_first_index - 1, char, L, tally_factor)
            tally_max = fast_rank(tally, char_last_index, char, L, tally_factor)

            if tally_max - tally_min == 0:
                break

            char_first_index = F[char] + tally_min
            char_last_index = char_first_index + tally_max - tally_min - 1
        else:
            for row in range(char_first_index, char_last_index + 1):
                match.append(resolve_fm_index_offset(SA, row, L, F, tally, tally_factor))
        
    return sorted(match)


def search(file: str, pattern: str, sa_factor: int = 1, tally_factor: int = 1):
    T = load_file(file)
    T += MARKER
    T_file = prepare_file(T)
    suffix_array = sais_suffix_array(T_file)

    L = burrows_wheeler_transform(T, suffix_array)
    F = first_column(L)
    SA = generate_suffix_array(T, sa_factor, suffix_array)
    tally = generate_tally(L, tally_factor)

    match = []

    first_column_chars = list(F)
    last_char_in_pattern_index = first_column_chars.index(pattern[-1])

    char_first_index = F[pattern[-1]] 
    if last_char_in_pattern_index < len(F) - 1:
        char_last_index = F[first_column_chars[last_char_in_pattern_index + 1]] - 1 
    else:
        char_last_index = len(L) - 1

    for pattern_index in range(len(pattern) - 1, -1, -1):
        if pattern_index > 0:
            char = pattern[pattern_index - 1]
            
            tally_min = fast_rank(tally, char_first_index - 1, char, L, tally_factor)
            tally_max = fast_rank(tally, char_last_index, char, L, tally_factor)

            if tally_max - tally_min == 0:
                break

            char_first_index = F[char] + tally_min
            char_last_index = char_first_index + tally_max - tally_min - 1
        else:
            for row in range(char_first_index, char_last_index + 1):
                match.append(resolve_fm_index_offset(SA, row, L, F, tally, tally_factor))
        
    return sorted(match)
