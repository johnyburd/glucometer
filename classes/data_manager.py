# This class manages the database for storing data, and calculates regressions and values with it
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from scipy.stats import linregress
from numpy import empty
import math
import datetime

class DataManager:
    def __init__(self):
        self.con = lite.connect('data.db')
        cur = self.con.cursor()
        # Table for storing date, time, blood glucose value, carbs, bolus, and notes
        cur.execute("CREATE TABLE IF NOT EXISTS Data(Id INTEGER PRIMARY KEY, DateColumn date, Bg INT, Carbs INT, Bolus INT, Notes Text)")
        # Table for storing points with which to calibrate the meter.
        cur.execute("CREATE TABLE IF NOT EXISTS CalibData(ADC INT, Actual INT)")

    # Adds a new data point to the "Data" table
    def new_entry(self, date, bg, carbs, bolus, notes):
        self.con.execute("INSERT INTO data(DateColumn, Bg, Carbs, Bolus, Notes)  VALUES ('"+date+"',"+str(bg)+","+str(carbs)+","+str(bolus)+",'"+notes+"')")
        self.con.commit()

    # Deletes an entry from the "Data" table  TODO why is this function here?
    def delete_entry(self, rowid):
        self.con.execute("DELETE from Data where Id=" + str(rowid))
        self.con.commit()

        print 'deleted ' + str(rowid)

    # Adds a new data point to the "CabibData" table
    def new_calib_entry(self, adc, actual):
        self.con.execute("INSERT INTO CalibData(ADC, Actual) VALUES ("+str(adc)+","+str(actual)+")")
        self.con.commit()

    # Calculates linear regression on the "CalibData" table in the database.  Returns line as a lambda object
    def get_line(self):
        rows = self.get_whole_table("CalibData")
        x = empty([len(rows)])
        y = empty([len(rows)])
        index = 0
        for row in rows:
            x[index] = row["ADC"]
            y[index] = row["Actual"]
            index += 1
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return lambda x: slope*x + intercept

    # Returns the requested table as a dictonary object
    def get_whole_table(self, table):
        with self.con:
            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            cur.execute("SELECT * FROM " + table)
#SELECT * FROM data ORDER BY datetime(dateColumn);


            return cur.fetchall()

    # Returns the requested table ordered by a column named datetime
    def get_whole_table_sorted(self, table): 
        with self.con:
            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            cur.execute("SELECT * FROM " + table + " ORDER BY datetime(dateColumn)")


            return cur.fetchall()

    # Deletes the sqlite table passed
    def delete_table(self, table):
        cur = self.con.cursor()
        cur.execute("DROP TABLE IF EXISTS " + table)

    # Sorts Table into chronological order TODO doesn't work
    def sort_data_table(self):
        data_table = self.get_whole_table('Data')
        datetime_list = []
        for entry in data_table:
            datetime_list.append(self.str_to_date(str(entry["Date"]),str(entry["Time"])))
        datetime_list.sort()
        #self.delete_table("Data")
        for entry in datetime_list:
            self.new
        return datetime_list

    # Converts strings in the format m/d/y or m/d/y, h:m to a datetime object TODO depreciated
    def str_to_date(self, strdate):
        if '/' in strdate:
            split_date = strdate.split('/')
            m = int(split_date[0])
            d = int(split_date[1])
            y = int(split_date[2])
            h = 0
            mins = 0
            if y < 100:
                y = int('20' + str(y))

        else:
            try:
                dateobj = datetime.datetime.strptime( strdate, "%Y-%m-%d %H:%M" )
                return dateobj
            except:
                pass
            try:
                dateobj = datetime.datetime.strptime( strdate, "%Y-%m-%d" )
                return dateobj
            except:
                pass

        return datetime.datetime(year=y, month=m, day=d, hour=h, minute=mins)

# Testing stuff
if __name__ == "__main__":
    bgm = DataManager()
    rows = bgm.get_whole_table("Data")

    data = (
        ('2016-01-24 23:45', 98, 36, 9, 'bg of 98'),
        ('2016-02-24 23:45', 94, 24, 6, 'same notes'),
        ('2016-04-24 23:45', 112, 26, 7, 'notes these are them'),
        ('2016-05-24 23:45', 86, 13, 3, 'aeu'),
        ('2016-03-24 23:45', 134, 6, 2, 'none'),
        ('2016-06-24 23:45', 99, 6, 2, 'it was 99 today'),
        ('2016-07-24 23:45', 109, 12, 3, 'tomorrow is 140'),
        ('2016-08-24 12:45', 103, 140, 35, 'wow thats high'),
        ('2016-09-24 23:45', 109, 60, 15, 'testing'),
        ('2016-12-24 23:45', 94, 44, 11, '44, 11'),
        ('2016-10-24 23:45', 117, 6, 2, 'notesnotesnotes'),
        ('2016-12-24 23:45', 117, 6, 2, 'notesnotesnotes'),
        ('2016-11-24 12:45', 111, 26, 7, ' '),
        ('2016-11-24 23:45', 117, 6, 2, 'notesnotesnotes'),
        ('2016-12-24 23:45', 111, 26, 7, ' '),
        ('2016-12-24 23:45', 111, 26, 7, ' ')
    )
    #table = bgm.sort_data_table()
    table = bgm.get_whole_table_sorted("Data")
    for thing in table:
        print thing

    #bgm.delete_table('Data')
    #bgm = DataManager()
    #for point in data:
    #    bgm.new_entry(point[0],point[1],point[2],point[3], point[4])
    #for row in rows:
       # print "%s %s %s" % (row["Date"], row["Bg"], row["Carbs"])
        #print point[0]
    #bgm.delete_table('calibdata')
    #bgm.new_calib_entry(1, 1)
    #bgm.new_calib_entry(20, -100)
    #test = bgm.get_line()
    #print test(3700)






