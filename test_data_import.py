import unittest
import data_import
import random
import os
from os import path
import datetime
import dateutil.parser

class TestDataImport(unittest.TestCase):

    def test_import_data_findfile(self):
        # we should be able to read an input file,
        # the file activity_small.csv
    
        r =  data_import.ImportData('activity_small.csv')
        self.assertEqual(r.file, './smallData/activity_small.csv')
        
    def test_import_data_readfile(self):
        # We should be able to read the first value in the file
        # from the file activity_small.csv

        r = data_import.ImportData('activity_small.csv')
        self.assertEqual(r._value[0], '0')
    
    def test_import_data_lowhigh(self):
        # high and low strings should be replaced with
        # 300 and 40, respectively

        r = data_import.ImportData('cgm_small.csv')
        self.assertEqual(r._value[285], 300)

    def test_import_data_timereader(self):
        # We should be able to read the time in the proper
        # format from the file activity_small.csv
        # To test this, we will observe a known dateutil parser

        r = data_import.ImportData('activity_small.csv')
        self.assertEqual((r._time[0]), dateutil.parser.parse('3/12/18 0:00'))

    def test_import_data_error(self):
        # if we try and parse a bad time, we should pass an error 
        with self.assertRaises(ValueError):
            r = data_import.ImportData('bad_time.csv')
        

if __name__ == '__main__':
    unittest.main()
