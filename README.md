# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data. 
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
from os.path import isfile, join
import argparse
import datetime
```

## Running the program
Specify an input folder, output text, and key file to parse time series data:
```python
python data_import.py smallData/ test.txt cgm_small.csv
```
## Release History
*1.0\
	*CHANGE: Functionality of ImportData class and RoundTime functions, as well as PrintArray capabilites
	*ADDED: Functional and Unit tests


## To Contribute
## To Contribute
1. Fork it (< https://github.com/cu-swe4s-fall-2019/time-series-basics-sahu0957.git>)
2. Create your feature branch (`git checkout -b feature_branch`)
3. Commit your changes (`git commit -m 'add your notes'`)
4. Push to the branch (`git push origin feature_branch`)
5. Create a new Pull request
