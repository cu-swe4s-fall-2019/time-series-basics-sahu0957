test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

#if the file doesn't exist, we should just exit with an error

run data_import_test python data_import.py foo test.txt cgm_small.csv
assert_exit_code 1

# try to run with proper inputs
run data_import_test python data_import.py smallData cgm_key cgm_small.csv
assert_exit_code 0

