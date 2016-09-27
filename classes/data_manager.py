# This class manages the database for storing data, and calculates regressions and values with it
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class DataManager:
    def __init__(self):
        self.con = lite.connect('test.db')

    # returns table in dict form
    def get_whole_table(self, table):
        with self.con:
            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            cur.execute("SELECT * FROM " + table)

            return cur.fetchall()

if __name__ == "__main__":
    bgm = BloodGlucoseManager()
    rows = bgm.get_whole_table("Cars")
    for row in rows:
        print "%s %s %s" % (row["Id"], row["Name"], row["Price"])  





