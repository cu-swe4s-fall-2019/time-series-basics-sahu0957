test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

# try to run with proper inputs
# For some reason my tests will run here, but not on Travis. Let's just
# comment everything out and see what happens...
run data_import python data_import.py smallData cgm_key cgm_small.csv
assert_exit_code 0

run data_error python data_import.py smallData cgm_key foo.csv
assert_exit_code 1
