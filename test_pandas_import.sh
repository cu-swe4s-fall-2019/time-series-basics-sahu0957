test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# checking errors, outputs of the scripts. Delete them if they exist
# to start
rm -f pandas_15min.csv
rm -f pandas_5min.csv

run data_import python pandas_import.py 
assert_exit_code 0

# Check to make sure the file got made
run file_checker ls 'pandas_15min.csv' 
assert_in_stdout 'pandas_15min.csv'
run file_checker_two ls 'pandas_5min.csv'
assert_in_stdout 'pandas_5min.csv'

# Check to make sure it's populated
run file_size_checker wc -l 'pandas_15min.csv'
assert_in_stdout 386

run file_size_checker_two wc -l 'pandas_5min.csv'
assert_in_stdout 1153
