import unittest
import data_import
import random
import os
from os import path


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
if __name__ == '__main__':
    unittest.main()
