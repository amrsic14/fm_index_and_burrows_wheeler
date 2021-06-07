from src.tally import fast_rank


def simple_suffix_array(T: str):
    def compare(a: int, b: int):
        compare, l = len(T), len(T)

        while True:
            compare = ord(T[a]) - ord(T[b])
            a += 1
            b += 1
            if a >= l:
                a -= l
            if b >= l:
                b -= l
            if compare != 0:
                break
        return compare
    
    array = [i for i in range(len(T))]
    import functools
    array.sort(key=functools.cmp_to_key(compare))

    return array


def generate_suffix_array(T: str, sa_factor: int = 1, array = None):
    if (sa_factor > len(T)):
        raise AssertionError("Suffix array factor bigger than length of text")
    
    if array is None:
        array = simple_suffix_array(T)

    suffix_array = {}

    for i in range(len(array)):
        if not(array[i] % sa_factor):
            suffix_array.update({i : array[i]})
        
    return suffix_array


def resolve_fm_index_offset(suffix_array, row, L, F, tally, tally_factor=1):
    if (tally_factor > len(L)):
        raise AssertionError("Tally factor bigger than length of BWT")
    
    step_cnt = 0
    
    while True:
        
        if row in suffix_array:
            break

        char = L[row]
        rank = fast_rank(tally, row, char, L, tally_factor) - 1
        row = F[char] + rank
        step_cnt += 1
    
    return suffix_array[row] + step_cnt
