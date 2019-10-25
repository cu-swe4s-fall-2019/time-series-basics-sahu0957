test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# try to run with proper inputs
run data_import_test python data_import.py smallData cgm_key cgm_small.csv
assert_exit_code 0

