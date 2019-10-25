# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data.

These scripts will take input data, and round the timestamp data in each of the input files. The rounded times and the corresponding data are combined into a CSV output file.
## Installation
You will need to use the following python modules as well as the following conda install for the ImportData class

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
~/miniconda3/etc/profile.d/conda.sh
conda update --yes conda
conda config --add channels r
conda create --yes -n test
conda activate test
conda install -y pycodestyle
conda install --yes python=3.6
conda install conda install -c conda-forge time
```
```python
import csv
import dateutil.parser
from os import listdir
import os.path
from os.path import isfile, join
import argparse
import datetime
import math
import copy
```

## Running the program
Specify an input folder, output text, and key file to parse time series data:
```python
python data_import.py /path/to/folder output_name key_file.csv
```
This will result in two data files, one that has rounded the times found in the specified key file, rounded to five and fifteen minutes. The other data files will be searched for times matching these rounded times, and will be included in the output file test_5.csv and test_15.csv (or specified name)

## Release History
*1.0\
	*CHANGE: Functionality of ImportData class and RoundTime functions, as well as PrintArray capabilites\
	*ADDED: Functional and Unit tests\
*2.0\
	*CHANGE: Fixed ImportData class, linear_search_value functions, and RoundTimeArray, PrintArray functions\
	*CHANGE: Updated functional and Unit tests to look at more edge/error cases\
	*ADDED: CSV files resulting from 5 and 15 minute rounding runs of the data_import.py script\


## To Contribute
1. Fork it (< https://github.com/cu-swe4s-fall-2019/time-series-basics-sahu0957.git>)
2. Create your feature branch (`git checkout -b feature_branch`)
3. Commit your changes (`git commit -m 'add your notes'`)
4. Push to the branch (`git push origin feature_branch`)
5. Create a new Pull request

## Source
A lot of the code here was adopted from our class lecture repo: cu-swe4s-fall-2019
