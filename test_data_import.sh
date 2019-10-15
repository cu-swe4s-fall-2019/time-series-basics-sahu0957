test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

run data_import_test python data_import.py smallData/ test.txt cgm_small.csv
assert_exit_code 0
