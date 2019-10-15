import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._roundval = []
        self._roundtime = []
        self._roundtimeStr = []
        self.file = data_csv 
        with open(self.file, "r") as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                if row['value'] == 'high':
                    print("Replacing value 'high' with 300")
                    self._value.append(300)
                elif row['value'] == 'low':
                    print("Replacing value 'low' with 40")
                    self._value.append(40)
                else:
                    self._value.append(row['value'])
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Can`t parse the time!')
                    print(row['time'])
            fhandle.close()
        # open file, create a reader from csv.DictReader, and read input times and values
        
    def linear_search_value(self, key_time):
        hit = -1
        for i in range(len(self._roundtime)):
            curr = self._roundtime[i]
            print(i)
            if key_time == curr:
                return self._value[i]
        return -1
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

    def binary_search_value(self,key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

def roundTimeArray(obj, res):
    f = 0
    for times in obj._time:
        minminus = datetime.timedelta(minutes = (times.minute % res))
        minplus = datetime.timedelta(minutes=res) - minminus
        if (times.minute % res) <= res/2:
            newtime = times - minminus
        else:
            newtime = times + minplus
        obj._roundtime.append(newtime)
        obj._roundtimeStr.append(newtime.strftime("%m/%d/%Y %H:%M"))
        obj._roundval.append(obj.linear_search_value(newtime))
        if len(obj._roundval[f]) > 1:
            if obj.file == './smallData/activity_small.csv':
                print(obj._roundval)
                #obj._roundval[i] = sum(int(obj._roundval[i]))
            if obj.file == './smallData/basal_small.csv':
                obj._roundval[f] = (sum(obj._roundval[f])/len(obj._roundval[f]))
            if obj.file == './smallData/bolus_small.csv':
                obj._roundval[f] = sum(obj._roundval[f])
            if obj.file == './smallData/cgm_small.csv':
                obj._roundval[f] = (sum(obj._roundval[f])/len(obj._roundval[f]))
            if obj.file == './smallData/hr_small.csv':
                obj._roundval[f] = (sum(obj._roundval[f])/len(obj._roundval[f]))
            if obj.file == './smallData/meal_small.csv':
                obj._roundval[f] = sum(obj._roundval[f])
            if obj.file == './smallData/smbg_small.csv':
                obj._roundval[f] = (sum(obj._roundval[f])/len(obj._roundval[f]))
        f += 1
    return(obj._roundval, obj._roundtime)
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned


def printArray(data_list, annotation_list, base_name, key_file):
    base_data = []
    key_idx = 0
    print(annotation_list)
    print(data_list)
    for i in range(len(annotation_list)):
        print(i)
        if annotation_list[i] == key_file:
            base_data = zip(data_list[i]._roundtimeStr, data_list[i]._value)
            print('base data is: '+annotation_list[i])
            key_idx = i
            break
        if i == len(annotation_list):
            print('Key not found')

    file=open(base_name+'.csv','w')
    file.write('time,')

    file.write(annotation_list[key_idx][0:-4]+', ')

    non_key = list(range(len(annotation_list)))
    non_key.remove(key_idx)

    for idx in non_key:
        file.write(annotation_list[idx][0:-4]+', ')
    file.write('\n')


    for time, value in base_data:
        file.write(time+', '+value+', ')
        for n in non_key:
            if time in data_list[n]._roundtimeStr:
                file.write(str(data_list[n].linear_search_value(time))+', ')
            else:
                file.write('0, ')
        file.write('\n')
    file.close() 
    # combine and print on the key_file

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()

    
    #pull all the folders in the file
    folder_path = args.folder_name
    files_lst = [f for f in listdir(folder_path) if isfile(join(folder_path, f))] # list the folders
    

    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for files in files_lst:
        data_lst.append(ImportData(folder_path+files))
    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min
    data_5 = roundTimeArray(data_lst[0], 5)
    data_15 = roundTimeArray(data_lst[0], 15)
    #print to a csv file
    printArray(data_5, files_lst,args.output_file+'_5',args.sort_key)
    printArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
