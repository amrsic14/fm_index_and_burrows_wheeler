import sys, os, time
from datetime import datetime
from src.tally import generate_tally
from src.suffix_array import generate_suffix_array, sais_suffix_array
from src.burrows_wheeler import MARKER, burrows_wheeler_transform, first_column
from src.search import search_benchmark
from Bio import SeqIO


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


def main():
    datasets = [
        {
            'file' : '7962_ref_common_carp_genome_chr10.fa',
            'patterns' : ['AGAACC', 'TCAAATC', 'TAACATCCAG']
        },
        {
            'file' : '13443_ref_Cara_1.0_chr1c.fa',
            'patterns' : ['ATGCATG', 'TCTCTCTA', 'TTCACTACTCTCA']
        },
        {
            'file' : '10093_ref_PAHARI_EIJ_v1.1_chrX.fa',
            'patterns' : ['ATGATG', 'CTCTCTA', 'TCACTACTCTCA']
        }
    ]

    sa_factors = [1, 4, 16, 64, 256]
    tally_factors = [1, 8, 32, 128, 512]

    for dataset in datasets:
        T_string = load_file(f"data/{dataset['file']}")
        T_string += MARKER
        T_file = prepare_file(T_string)
        print(f'Working with: {dataset["file"]}')
        
        out_file = open(f'data/{dataset["file"].rpartition(".")[0]}_benchmark.txt', 'w')
        out_file.write(f'\n\n\n******************** {dataset["file"].rpartition(".")[0]} ********************\n\n\n')

        bwt_start_time = time.time()
        array = sais_suffix_array(T_file)

        L = burrows_wheeler_transform(T_string, array)
        bwt_time = time.time() - bwt_start_time
        out_file.write(f'time: {bwt_time:.3f}s\n\n')
        
        F = first_column(L)
        bwt_memory = sys.getsizeof(array) + sys.getsizeof(L) + sys.getsizeof(F)

        for sa_factor in sa_factors:

            SA = generate_suffix_array(T_file, sa_factor, array)
            sa_memory = sys.getsizeof(SA)

            for tally_factor in tally_factors:

                tally = generate_tally(L, tally_factor)
                tally_memory = sys.getsizeof(tally)

                out_file.write(f'====================================================\n')
                out_file.write(f'sa_factor: {sa_factor}    tally_factor: {tally_factor}\n')

                out_file.write(f'memory: {(bwt_memory + sa_memory + tally_memory) / 2. ** 20:.3f}MB\n')

                for pattern in dataset['patterns']:
                    start_time_pattern = time.time()
                    matches = search_benchmark(pattern, F, L, SA, tally, tally_factor)
                    end_time_pattern = time.time()
                    out_file.write(
                        f'{pattern:<10}: {(end_time_pattern - start_time_pattern) * 1000:.3f}ms '
                        f'\t\t matches: {len(matches):<3}\n')

                out_file.write(f'====================================================\n')

        os.remove(T_file)
        out_file.close()
        print(f'Finished: {dataset["file"]}')


if __name__ == '__main__':
    main()
