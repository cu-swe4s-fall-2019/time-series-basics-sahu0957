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
    
        r =  data_import.ImportData('./smallData/activity_small.csv')
        self.assertEqual(r.file, './smallData/activity_small.csv')
        
    def test_import_data_readfile(self):
        # We should be able to read the first value in the file
        # from the file activity_small.csv

        r = data_import.ImportData('./smallData/activity_small.csv')
        self.assertEqual(r._value[0], 0)
    
    def test_import_data_lowhigh(self):
        # high and low strings should be replaced with
        # 300 and 40, respectively

        r = data_import.ImportData('./smallData/cgm_small.csv')
        self.assertEqual(r._value[285], 300)

    def test_import_data_timereader(self):
        # We should be able to read the time in the proper
        # format from the file activity_small.csv
        # To test this, we will observe a known dateutil parser

        r = data_import.ImportData('./smallData/activity_small.csv')
        self.assertEqual((r._time[0]), dateutil.parser.parse('3/12/18 0:00'))

    def test_import_data_error(self):
        # if we try and parse a bad time, we should pass an error 
        with self.assertRaises(ValueError):
            r = data_import.ImportData('./bad_time.csv')

    def test_roundtime_array(self):
        # we should be able to make the same array if we have a resolution
        # of one
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 1)
        self.assertEqual(r._roundtime, r._time)

    def test_roundtime_array(self):
        # With a resolution of 3, our new array round the first entries together
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 3)
        self.assertEqual(r._roundtime[0], r._roundtime[1])
   
    def test_linear_search_roundtime(self):
        # Linear search of the rounded table should return 2 entries for the first one
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 3)
        w = r.linear_search_value(r._time[0])
        # For activity_small, should return a sum of 0
        self.assertEqual(w, 0)

    def test_linear_search_roundtime_sum(self):
        # Linear search of forty minute rounding, which should be a sum of 99
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 40)
        w = r.linear_search_value(r._time[0])
        self.assertEqual(w, 99)

    def test_linear_search_roundtime_avg(self):
        # Linear search of forty minute rounding, which should be an avg of 138
        r = data_import.ImportData('./smallData/cgm_small.csv')
        data_import.roundTimeArray(r, 9)
        w = r.linear_search_value(r._time[1])
        self.assertEqual(w, 138)

    def test_linear_search_first(self):
        # Given a specific time, we should return the proper value
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 1)
        w = r.linear_search_value(r._time[0]) 
        self.assertEqual(r._value[0], w)

    def test_linear_search_last(self):
        # See if the last entry matches
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 1)
        w = r.linear_search_value(r._time[4])
        self.assertEqual(r._value[4], w)

    def test_linear_search_doubledigits(self):
        # To make sure it's handling double digits okay, I choese
        # to return a double digit entry
        r = data_import.ImportData('./smallData/activity_small.csv')
        data_import.roundTimeArray(r, 1)
        w = r.linear_search_value(r._time[14])
        self.assertEqual(r._value[14], w)
    
if __name__ == '__main__':
    unittest.main()
