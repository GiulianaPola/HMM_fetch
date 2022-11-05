# HMM-fetch: A tool to select profile HMMs from a database

HMM-fetch is a Python script that uses a list of names of HMMs and a file of concatenated profile HMMs. From the names of the profile HMMs in the list, HMM-fetch searches the profile HMM database and saves the selected profile HMM to a file with its name. Finally the program creates a log file that describes its execution and creates a concatenated file of the selected profile HMMs.

## Instalation

HMM-Prospector also does not need to be installed. The user should only download the hmm-prospector.py file.

## Requirements

- 

## Usage

```
python hmm_fetch.py -i <list file> -d <hmm file> <optional parameters>
```  

### Mandatory parameters:

```
-i  <text file>        : Profile HMM namelist
-d  <hmm concated file>        : Profile HMM dataset
```

### Optional parameters:

```
-o             	  : Output directory (default = hmm_fetch).
```

## Contact

To report bugs, to ask for help and to give any feedback, please contact Arthur Gruber (argruber@usp.br) or Giuliana L. Pola (giulianapola@usp.br).

