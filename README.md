# Burrows-Wheeler transformation and FM index

This implementation of the Burrows-Wheeler transformation and FM index was done as a project assignment for the Genome Informatics course at the Faculty of Electrical Engineering in Belgrade.

## How to use 

The main module of this assignment is ```main.py```.
You can either use it for benchmarking results of searching patterns in the predefined fasta files or you can use it for searching patterns in your fasta files.

## Suffix array

For sufix array generation is used 'sais' algorithm from https://sites.google.com/site/yuta256/sais

### Arguments for the main module

|     Argument       |              Description                | Required | Default value |
|--------------------|-----------------------------------------|----------|---------------|
|--do_benchmark, -b  |   Do benchmark                          |    No    |     -         |
|--file, -f          |   Path to fasta file                    |    Yes   |     -         |
|--pattern, -p       |   Pattern to look for in fasta file     |    Yes   |     -         |
|--sa_factor, -sf    |   Suffix array factor                   |    No    |     1         |
|--tally_factor, -tf |   Tally matrix factor                   |    No    |     1         |

Note: If benchmark is activated only it will be performed and there is no need to add other required arguments.

Example commands:
```python main.py -b```\
```python main.py -f ../data/fasta_file.fa -p ACTGAC ```\
```python main.py -f ../data/fasta_file.fa -p ACTGAC -tf 512```\
```python main.py -f ../data/fasta_file.fa -p ACTGAC -tf 512 --sa_factor 4```\

## Test

To run unit test, position yourself in the src directory and run the following command: ```python -m unittest discover```

## Benchmar

Benchmark results are stored in the data directory with the name 'genom_file_name_benchmark.txt'

## Presentation

Link to the YouTube video: https://youtu.be/mWR1NHwDkGY
