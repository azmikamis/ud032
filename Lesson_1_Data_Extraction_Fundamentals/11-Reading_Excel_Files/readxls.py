﻿#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min and max values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import os
import xlrd
from zipfile import ZipFile
DATADIR = "Lesson_1_Data_Extraction_Fundamentals\\11-Reading_Excel_Files"
DATAFILE = "2013_ERCOT_Hourly_Load_Data"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook('{0}.xls'.format(os.path.basename(datafile)))
    sheet = workbook.sheet_by_index(0)

    ### example on how you can get the data
    #sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)
    coasts = zip(sheet.col_values(0, start_rowx=1),
                      sheet.col_values(1, start_rowx=1))
    mincoast = min(coasts, key=lambda x:x[1])
    maxcoast = max(coasts, key=lambda x:x[1])
    
    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):", 
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)
    mintime = xlrd.xldate_as_tuple(mincoast[0], 0)
    minvalue = mincoast[1]
    maxtime = xlrd.xldate_as_tuple(maxcoast[0], 0)
    maxvalue = maxcoast[1]
    
    avgcoast = sum([coast[1] for coast in coasts]) / len(coasts)
    
    data = {
            'maxtime': maxtime,
            'maxvalue': maxvalue,
            'mintime': mintime,
            'minvalue': minvalue,
            'avgcoast': avgcoast
    }
    return data


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()