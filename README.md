# HMM-fetch: A tool to select profile HMMs from a database

**Introduction:**
hmm_fetch.py is a command-line tool designed to fetch Profile Hidden Markov Models (HMMs) from a dataset based on a list of HMM names. This README provides detailed instructions on the installation, requirements, and usage of hmm_fetch.py.

**Installation:**
- There is no traditional installation process for hmm_fetch.py. Simply download the script and ensure you have the necessary dependencies.

**Requirements:**
- Python 3
- Standard Python libraries
- Operating system compatible with Python 3

**Usage:**
- Command Line Syntax: `python hmm_fetch.py -i <list file> -d <hmm file> [-o <output directory>]`
- Replace `<list file>` with the path to the file containing the list of HMM names.
- Replace `<hmm file>` with the path to the Profile HMM dataset.
- Optional: Use `-o <output directory>` to specify the output directory name.

**Mandatory Parameters:**
- `-i <list file>`: Profile HMM name list file.
- `-d <hmm file>`: Profile HMM dataset file.

**Optional Parameters:**
- `-o <output directory>`: Output directory name (default: hmm_selected).

**Reference:**
For academic references related to hmm_fetch.py, please visit https://github.com/GiulianaPola/HMM_fetch for more information on citing the tool in your publications.

**Contact:**
To report bugs, to ask for help and to give any feedback, please contact Arthur Gruber (argruber@usp.br) or Giuliana Pola (giulianapola@usp.br)
