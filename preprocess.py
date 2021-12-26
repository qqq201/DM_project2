import argparse
import csv
import math

def correct_datatype(c):
    '''
        convert string to its true datatype
    '''
    if not(c and c.strip()) or c == 'NA':
        return None
    try:
        if str(float(c)) == c: return float(c)
    except TypeError: return c
    except ValueError: return c

    try:
        if str(int(c)) == c: return int(c)
    except TypeError: return c
    except ValueError: return c


def mean(arr):
    '''
        find mean from array
    '''
    n = 0
    sum = 0

    # calculate mean
    for i in range(len(arr)):
        if arr[i] is not None:
            sum += arr[i]
            n += 1

    return sum / n

def mode(arr):
    '''
        find mode from array
    '''
    # calculate frequency of each value in array
    Dict = {}

    for value in arr:
        if value is not None:
            if value in Dict:
                Dict[value] = Dict[value] + 1
            else:
                Dict[value] = 1

    # find value with maximum frequency
    m = 0
    s = ""
    for key in Dict:
        if Dict[key] > m and key is not None:
            s = key
            m = Dict[key]

    return s


def min(arr):
    '''
        find min of array
    '''
    if arr != None:
        m = arr[0]
        for i in arr:
            if i < m:
                m = i

    return m


def max(arr):
    '''
        find max of array
    '''
    if arr != None:
        m = arr[0]
        for i in arr:
            if i > m:
                m = i

    return m


def standard_deviation(arr, mean, n):
    '''
        calculate standard_deviation from array
    '''
    if mean is None:
        mean = mean(arr)

    s = 0
    for i in range(n):
        s += (arr[i] - mean)**2
    return math.sqrt(s / n)


def attribute_type(arr):
    '''
        find datatype of array
    '''
    for value in arr:
        if value is not None:
            return type(value)
    return None


class Dataframe:
    def __init__(self):
        self.data = []  # 2D array
        self.attributes = [] # name


    def load_csv(self, file):
        with open(file, newline='') as f:
            # read data as 2d list
            reader = csv.reader(f)
            self.data = list(reader)
            self.attributes = self.data[0]

        n = len(self.data)
        m = len(self.data[0])
        self.data = [[correct_datatype(self.data[r][c]) for c in range(m)] for r in range(1, n)]



    def save_csv(self, file):
        with open(file, 'w', newline='') as f:
            write = csv.writer(f)
            # write the header
            write.writerow(self.attributes)

            # write data
            write.writerows(self.data)


    def get_column(self, attr):
        '''
            get a column based on attribute name
        '''
        index = 0
        try:
            index = self.attributes.index(attr)
        except ValueError:
            print(f"Does not exist {attr}")
            return None

        return [row[index] for row in self.data]


    def impute(self, output_file=None):
        '''
            handle impute
        '''
        for attr in self.attributes:
            column = self.get_column(attr)

            if column is not None:
                datatype = attribute_type(column)

                substitute = None
                if datatype == str:
                    substitute = mode(column)
                elif datatype == float or datatype == int:
                    substitute = mean(column)
                else:
                    continue

                c = self.attributes.index(attr)
                for r in range(len(column)):
                    if column[r] is None:
                        self.data[r][c] = substitute

        # save file
        if output_file:
            self.save_csv(output_file)


    def switch_to_last(self, attr):
        '''
            switch an attribute to be the last attribute
        '''
        c = self.attributes.index(attr)
        for r in range(len(self.data)):
            self.data[r][c], self.data[r][-1]= self.data[r][-1], self.data[r][c]

        self.attributes[c], self.attributes[-1]= self.attributes[-1], self.attributes[c]


df = Dataframe()

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file", type=str)
parser.add_argument("output", help="Output file", type=str)

args = parser.parse_args()

if args.input is not None:
    df.load_csv(args.input)
    df.switch_to_last('Species')

    if args.output is not None:
        df.impute(args.output)
