import csv
import dateutil.parser
import os.path
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import copy
import sys

class ImportData:
    def __init__(self, data_csv):
        self._data_list = []
        self._time = []
        self._value = []
        # Determine if we will average or sum the data collisions later
        if 'activity' in data_csv:
            self._type = 0
        if 'bolus' in data_csv:
            self._type = 0
        if 'meal' in data_csv:
            self._type = 0
        if 'smbg' in data_csv:
            self._type = 1
        if 'hr' in data_csv:
            self._type = 1
        if 'cgm' in data_csv:
            self._type = 1
        if 'basal' in data_csv:
            self._type = 1

        self.file = data_csv 

        with open(self.file, "r") as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                if (row['time'] == ''):
                    continue
                try:
                    time_toadd = (datetime.datetime.strptime(row['time'], '%m/%d/%y %H:%M'))
                except ValueError:
                    print('this time is the wrong format!')
                    sys.exit()
                try:
                    if row['value'] == 'high':
                        print("Replacing value 'high' with 300")
                        row['value'] = 300
                    elif row['value'] == 'low':
                        print("Replacing value 'low' with 40")
                        row['value'] = 40
                    
                    value_toadd = float(row['value'])
                    # if our number works, add it to the growing array
                    if (not math.isnan(value_toadd)):
                        self._value.append(value_toadd)
                        self._time.append(time_toadd)
                except ValueError:
                    print("can't parse the time! skipping entry")
            fhandle.close()
        # the data frame might get built backwards depending on the file
        # so just reverse it if that happens

        if len(self._time) > 0:
            if self._time[-1] < self._time[0]:
                self._time.reverse()
                self._value.reverse()

    def linear_search_value(self, key_time):
        hits = []
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                hits.append(self._value[i])
        if len(hits) == 0:
            print ('no results found')
            return -1
        
        return hits
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

def roundTimeArray(obj, resolution):
    # So this is on the example that you guys made, but I'm not sure why... 
    # I need to make a deep copy of the object
    # before I can mutate it by rounding the time
    rounded_obj = copy.deepcopy(obj)
    round_time = []
    values = []
    number_of_times = len(rounded_obj._time)

    for i in range(number_of_times):
        new_time = rounded_obj._time[i]
        remover = datetime.timedelta(minutes=new_time.minute % resolution,
                                     seconds=new_time.second)
        new_time -= remover
        if (remover >= datetime.timedelta(minutes = math.ceil(resolution/2))):
            new_time += datetime.timedelta(minutes=resolution)
        rounded_obj._time[i] = new_time
    
    if number_of_times > 0:
        round_time.append(rounded_obj._time[0])
        linear_search = rounded_obj.linear_search_value(rounded_obj._time[0])
        if obj._type == 0:
            values.append(sum(linear_search))
        elif obj._type == 1:
            values.append(sum(linear_search)/len(linear_search))

    for i in range(1, number_of_times):
        # To avoid duplications, look for where the number changes, and only include
        # one copy of that time
        if rounded_obj._time[i] == rounded_obj._time[i - 1]:
            continue
        else:
            round_time.append(rounded_obj._time[i])
            linear_search = rounded_obj.linear_search_value(rounded_obj._time[i])
            if obj._type == 0:
                values.append(sum(linear_search))
            elif obj._type == 1:
                values.append(sum(linear_search)/len(linear_search))
    return zip(round_time, values)


def printArray(data_list, annotation_list, base_name, key_file):
    data_list_main = []
    data_list_secondary = []
    annotation_list_main = []
    annotation_list_secondary = []

    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            annotation_list_main.append(annotation_list[i])
            data_list_main.append(data_list[i])
        else:
            annotation_list_secondary.append(annotation_list[i])
            data_list_secondary.append(data_list[i])

    attribute_order = ['time', key_file] + annotation_list_secondary
    with open(base_name + '.csv', mode = 'w') as out:
        writer = csv.writer(out, delimiter = ',')
        writer.writerow(attribute_order)
        for time, value in data_list_main[0]:
            other_values = []
            for data in data_list_secondary:
                old_len = len(other_values)
                for zip_time, zip_val in data:
                    if time == zip_time:
                        other_values.append(zip_val)
                    if len(other_values) == old_len:
                        other_values.append(0)
                writer.writerow([time, value] + other_values)

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'Combines data from a time series into a single file.',
    prog= 'dataImport')
    
    parser.add_argument('folder_name', type=str, help = 'Name of input folder')
    parser.add_argument('output_file', type=str, help = 'Name of Output file')
    parser.add_argument('sort_key', type=str, help = 'File to sort from')

    args = parser.parse_args()
    
    # Pull the files together from the folder
    try:
        files_lst = listdir(args.folder_name)
    except FileNotFoundError as e:
        print('Folder not found')
        sys.exit(1)
    
    for i in files_lst:
        if os.path.exists(args.folder_name + '/' + args.sort_key) == False:
            print('Key file not found')
            sys.exit(1)
    # Combine files into a list of ImportData objects
    data_lst = []
    for files in files_lst:
        data_lst.append(ImportData(args.folder_name + '/' + files))

    if len(data_lst) == 0:
        print('data list is empty!')
        sys.exit(1)

    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min

    for objs in data_lst:    
        data_5.append(roundTimeArray(objs, 5))
    for objs in data_lst:
        data_15.append(roundTimeArray(objs, 15))
    
    
    #print to a csv file
    
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
