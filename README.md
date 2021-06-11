# Burrows-Wheeler transformation and FM index

This implementation of the Burrows-Wheeler transformation and FM index was done as a project assignment for the Genome Informatics course at the Faculty of Electrical Engineering in Belgrade.

## How to use 

The main module of this assignment is ```main.py```.
You can either use it for benchmarking results of searching patterns in the predefined fasta files or you can use it for searching patterns in your fasta files.

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
```python main.py -b```
```python main.py -f ../data/fasta_file.fa -p ACTGAC ```
```python main.py -f ../data/fasta_file.fa -p ACTGAC -tf 512```
```python main.py -f ../data/fasta_file.fa -p ACTGAC -tf 512 --sa_factor 4```

## Test

To run unit test, position yourself in the src directory and run the following command: ```python -m unittest discover```

## Presentation

ADD LINK