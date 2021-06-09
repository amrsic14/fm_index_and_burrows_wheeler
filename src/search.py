from src.burrows_wheeler import MARKER, burrows_wheeler_transform, first_column
from src.tally import fast_rank, generate_tally
from src.suffix_array import generate_suffix_array, resolve_fm_index_offset, simple_suffix_array


def search_benchmark(pattern, F, L, SA, tally, tally_factor):
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


def search(T: str, pattern: str, sa_factor: int = 1, tally_factor: int = 1):
    T += MARKER

    array = simple_suffix_array(T)
    L = burrows_wheeler_transform(T, array)
    F = first_column(L)
    SA = generate_suffix_array(T, sa_factor, array)
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