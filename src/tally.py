def generate_tally(L: str, tally_factor: int = 1):
    if (tally_factor > len(L)):
        raise AssertionError("Tally factor bigger than length of L")
    
    chars = sorted(set(L))
    from src.burrows_wheeler import MARKER
    chars.remove(MARKER)
    
    chars_cnt = dict(zip(iter(chars), [0]*len(chars)))

    tally = []
    
    for i in range(len(L)):
        char = L[i]
        
        if char != MARKER:
            chars_cnt[char] += 1
        
        if i % tally_factor == 0:                
            tally.append(chars_cnt.copy())
            
    return tally


def fast_rank(tally, checkpoint: int, char: str, L: str, tally_factor: int = 1):
    if (tally_factor > len(L)):
        raise AssertionError("Tally factor bigger than length of L")
    
    nearest_checkpoint = int(round(checkpoint / tally_factor))
    
    if nearest_checkpoint == len(tally) and checkpoint % tally_factor:
        nearest_checkpoint -= 1
    
    rank = tally[nearest_checkpoint][char]
    
    if checkpoint % tally_factor:
        if nearest_checkpoint * tally_factor < checkpoint:
            lower_bound = nearest_checkpoint * tally_factor + 1
            upper_bound = checkpoint + 1
        else:
            lower_bound = checkpoint + 1
            upper_bound = nearest_checkpoint * tally_factor + 1
            
        
        for L_char in L[lower_bound:upper_bound]:
            if L_char == char:
                if nearest_checkpoint * tally_factor < checkpoint:
                    rank += 1
                else:
                    rank -= 1

    return rank
