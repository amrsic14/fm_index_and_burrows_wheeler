import sys
from datetime import datetime
from src.tally import generate_tally
from src.suffix_array import generate_suffix_array, simple_suffix_array
from src.burrows_wheeler import MARKER, burrows_wheeler_transform, first_column
from src.search import search_benchmark


def load_file(file_path: str):
    file = open(file_path, 'r')
    file.readline()
    data = file.read().replace('\n', '')
    file.close()
    return data


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

    out_file = open('data/benchmark.txt', 'w')

    for dataset in datasets:
        T = load_file(f"data/{dataset['file']}")
        print(f'Working with: {dataset["file"]}')
        
        out_file.write(f'\n\n\n**************** {dataset["file"].rpartition(".")[0]} ****************\n\n\n')

        T += MARKER

        bwt_start_time = datetime.now()
        array = simple_suffix_array(T)
        L = burrows_wheeler_transform(T, array)
        bwt_time = (datetime.now() - bwt_start_time).total_seconds()
        out_file.write(f'time: {bwt_time}s\n\n')
        
        F = first_column(L)
        bwt_memory = sys.getsizeof(array) + sys.getsizeof(L) + sys.getsizeof(F)

        for sa_factor in sa_factors:

            SA = generate_suffix_array(T, sa_factor, array)
            sa_memory = sys.getsizeof(SA)

            for tally_factor in tally_factors:

                tally = generate_tally(L, tally_factor)
                tally_memory = sys.getsizeof(tally)

                out_file.write(f'=======================================\n')
                out_file.write(f'sa_factor: {sa_factor}    tally_factor: {tally_factor}\n')

                out_file.write(f'memory: {(bwt_memory + sa_memory + tally_memory) / 2. ** 20}MB\n')

                for pattern in dataset['patterns']:
                    start_time_pattern = datetime.now().timestamp()
                    search_benchmark(pattern, F, L, SA, tally, tally_factor)
                    out_file.write(f'{pattern}: {(datetime.now().timestamp() - start_time_pattern) * 1000}ms\n')

                out_file.write(f'=======================================\n')

        print(f'Finished: {dataset["file"]}')

    out_file.close()


if __name__ == '__main__':
    main()
