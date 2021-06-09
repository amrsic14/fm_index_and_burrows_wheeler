from unittest import TestCase
from src.suffix_array import generate_suffix_array, resolve_fm_index_offset
from src.tally import fast_rank, generate_tally
from src.burrows_wheeler import burrows_wheeler_transform, first_column
from src.search import search


class Test_TestStringSearching(TestCase):

    def test_bwt(self):
        """ Test suffix array generation """

        self.assertEqual(burrows_wheeler_transform('banana$'), 'annb$aa')
        self.assertEqual(burrows_wheeler_transform('six_sleek_swans_swam_swiftly_southwards$'), 
                                                   'sxyskmwwwrleitwsestaasadn$_____ufosshsil')
        self.assertEqual(burrows_wheeler_transform('twelve_twins_twirled_twelve_twigs$'), 
                                                   'sdeesevvlwwiwwwreeiign_$___llttttt')

    def test_first_column(self):
        """ Test generation of BWT's first column """

        self.assertEqual(first_column(burrows_wheeler_transform('banana$')), {'a': 1, 'b': 4, 'n': 5})
        self.assertEqual(first_column(burrows_wheeler_transform('twelve_twins_twirled_twelve_twigs$')), 
        {'_': 1, 'd': 5, 'e': 6, 'g': 11, 'i': 12, 'l': 15, 'n': 18, 'r': 19, 's': 20, 't': 22, 'v': 27, 'w': 29})

    def test_tally_generation(self):
        """ Test generation of Tally table """

        L = burrows_wheeler_transform('banana$')

        self.assertEqual(generate_tally(L),
                        [{'a': 1, 'b': 0, 'n': 0}, 
                         {'a': 1, 'b': 0, 'n': 1}, 
                         {'a': 1, 'b': 0, 'n': 2}, 
                         {'a': 1, 'b': 1, 'n': 2}, 
                         {'a': 1, 'b': 1, 'n': 2}, 
                         {'a': 2, 'b': 1, 'n': 2}, 
                         {'a': 3, 'b': 1, 'n': 2}])
        self.assertEqual(generate_tally(L, tally_factor=2),
                        [{'a': 1, 'b': 0, 'n': 0}, 
                         {'a': 1, 'b': 0, 'n': 2}, 
                         {'a': 1, 'b': 1, 'n': 2}, 
                         {'a': 3, 'b': 1, 'n': 2}])
        self.assertEqual(generate_tally(L, tally_factor=5),
                        [{'a': 1, 'b': 0, 'n': 0},
                         {'a': 2, 'b': 1, 'n': 2}])

        self.assertRaises(AssertionError, generate_tally, L, 20)

    def test_fast_rank(self):
        """ Test fast rank calculation """

        L = burrows_wheeler_transform('banana$')
        tally_table_factor_1 = generate_tally(L)

        for tally_factor in range(1, len(L) + 1):
            
            tally_table = generate_tally(L, tally_factor)
            
            tally = []
            
            for checkpoint in range(len(L)):
                tally.append(
                    { 
                        'a': fast_rank(tally_table, checkpoint, 'a', L, tally_factor),
                        'b': fast_rank(tally_table, checkpoint, 'b', L, tally_factor),
                        'n': fast_rank(tally_table, checkpoint, 'n', L, tally_factor),
                    }
                )
            
            self.assertEqual(tally, tally_table_factor_1)

    def test_suffix_array(self):
        """ Test generation of suffix array """

        T = 'banana$'

        self.assertEqual(generate_suffix_array(T), {0: 6, 1: 5, 2: 3, 3: 1, 4: 0, 5: 4, 6: 2})
        self.assertEqual(generate_suffix_array(T, sa_factor=3), {0: 6, 2: 3, 4: 0})
        self.assertEqual(generate_suffix_array(T, sa_factor=6), {0: 6, 4: 0})

        self.assertRaises(AssertionError, generate_suffix_array, T, 20)

    def test_fm_index_offset(self):
        T = 'banana$'
        suffix_array_factor_1 = generate_suffix_array(T)

        for sa_factor in range(1, len(T) + 1):

            suffix_array_helper = generate_suffix_array(T, sa_factor)
            L = burrows_wheeler_transform(T)
            F = first_column(L)
            tally_table = generate_tally(L)
            
            suffix_array = {}
            
            for row in range(len(T)):
                suffix_array[row] = resolve_fm_index_offset(suffix_array_helper, row, L, F, tally_table)
            
            self.assertEqual(suffix_array, suffix_array_factor_1)

    def test_search(self):
        self.assertEqual(search('banana', 'na'), [2,4])
        self.assertEqual(search('ffffff', 'f' , 1, 3), [0, 1, 2, 3, 4, 5])
        self.assertEqual(search('six_sleek_swans_swam_swiftly_southwards', 'eek_' , 3, 2), [6])
        self.assertEqual(search('find nothing', 'gi', 2, 2), [])
        self.assertEqual(search('na', 'banana'), [])
        self.assertEqual(search('whole_word', 'whole_word', 4, 4), [0])
        self.assertEqual(search('last_char', 'r'), [8])
