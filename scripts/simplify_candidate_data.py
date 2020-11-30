# !/user/local/bin/python2.7
# -*- coding: utf-8 -*-

import csv
import sys

from constants import *
from utils.unicode_utils import *

SCHOOL_YEAR = {
    'Năm thứ nhất': 1, 'Năm thứ hai': 2, 'Khác': 3
}


def city(string1, string2):
    if string1 == '' or string2 == '':
        return ''
    else:
        return titlestyle(string1) \
                   .replace('Huyện ', '') \
                   .replace('Quận ', '') \
                   .replace('Thị Xã ', '') \
                   .replace(',', '-') \
               + "; " + string2


def transformCSVToList(filename):
    with open(os.path.abspath(filename), 'rU', encoding='utf-8') as f:
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
        f.close()
    return data


def simplify(record, semester):
    new_record = [""] * 12
    fullname = titlestyle(record[1]).split(" ")
    new_record[0] = str(semester) + SCHOOL_NB.get(record[8], '21')
    new_record[1] = " ".join(fullname[:-1])
    new_record[2] = fullname[-1]
    new_record[3] = record[2]
    new_record[4] = record[3]
    new_record[5] = SCHOOL_YEAR[record[5]] if record[5] in SCHOOL_YEAR else ""
    new_record[6] = record[7].replace(',', ';')
    new_record[7] = SCHOOL_CODE_ALL.get(record[8], 'KHAC')
    new_record[8] = city(record[10], record[11])
    new_record[9] = record[16]
    new_record[10] = record[15]
    # last column is for result
    return new_record


def getKeyToCompare(item):
    return item[7].ljust(10, '0') + item[2].ljust(12, '0') + item[1].ljust(40, '0')


if __name__ == '__main__':
    data = transformCSVToList(sys.argv[1])
    semester = sys.argv[2]
    newdata = []
    for i in range(1, len(data)):
        res = simplify(data[i], semester)
        newdata.append(res)
    newdata = sorted(newdata, key=getKeyToCompare)
    myfile = open(sys.argv[1][:-4] + '_Simplified.csv', 'w')
    for i in range(len(newdata)):
        myfile.write(newdata[i][0])
        for j in range(1, len(newdata[0])):
            myfile.write(',')
            myfile.write(str(newdata[i][j]))
        myfile.write('\n')
    myfile.close()
    print("Successfully finished.")
