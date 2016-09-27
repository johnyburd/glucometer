# This class manages the database for storing data, and calculates regressions and values with it
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class DataManager:
    def __init__(self):
        self.con = lite.connect('data.db')
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Data(Id INTEGER PRIMARY KEY, Date TEXT, Bg INT, Carbs INT, Bolus INT)")


    def new_entry(self, date, bg, carbs, bolus):

        self.con.execute("INSERT INTO data(Date, Bg, Carbs, Bolus)  VALUES ('"+date+"',"+str(bg)+","+str(carbs)+","+str(bolus)+")")
        self.con.commit()
    def delete_entry(self, rowid):
        self.con.execute("DELETE from Data where Id=" + str(rowid))

    # returns table in dict form
    def get_whole_table(self, table):
        with self.con:
            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            print cur
            cur.execute("SELECT * FROM " + table)

            return cur.fetchall()
    def delete_table(self):
        cur = self.con.cursor()
        cur.execute("DROP TABLE IF EXISTS Data")

if __name__ == "__main__":
    bgm = DataManager()
    rows = bgm.get_whole_table("Data")

    data = (
        ('9/1/16', 98, 36, 9),
        ('9/2/16', 94, 24, 6),
        ('9/4/16', 112, 26, 7),
        ('9/6/16', 86, 13, 3),
        ('9/6/16', 134, 6, 2),
        ('9/7/16', 99, 6, 2),
        ('9/7/16', 109, 12, 3),
        ('9/8/16', 103, 140, 35),
        ('9/15/16', 109, 60, 15),
        ('9/20/16', 94, 44, 11),
        ('9/23/16', 117, 6, 2),
        ('9/24/16', 111, 26, 7)
    )

    for point in data:
        bgm.new_entry(point[0],point[1],point[2],point[3])
    for row in rows:
        print "%s %s %s" % (row["Date"], row["Bg"], row["Carbs"])
        #print point[0]
    #bgm.delete_table()






