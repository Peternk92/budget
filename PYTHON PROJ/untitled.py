#ToDO - Make sure you can see a list of percentages of money that you spend in each category

#CHANGE DATETIME TO STRING
#temp = today.strftime('%Y-%m-%d')
#print temp

#!/usr/bin/python


import cal
import datetime
from datetime import date
import time
import csv

class budget():
    today = date.today()
    first_date = date.today()
    new_file_flag = False
    
    def __init__(self):
        #if file exists, check last entry to see if up to date.
        #if last entry is not today, add days until today.
        if(FileCheck("data.csv") == True):
            print "Loading in file..."
            data = csv.reader(open("data.csv", "rU"))
            num_rows = sum(1 for row in data)
            data = csv.reader(open("data.csv", "rU"))
            data = list(data)
            #check last entry
            if(data[num_rows-1][0] == today.strftime("%Y-%m-%d")):
                print "up to date!"
            else:
                last_date_list = data[num_rows-1][0].split("-")
                #converts to year month day date (passed in as such)
                last_known_date = date(int(last_date_list[0]),int(last_date_list[1]),int(last_date_list[2]))
                num_days_between = (today - last_known_date).days
                with open("data.csv","a") as datafile:  
                    file = csv.writer(datafile, delimiter=',',quoting=csv.QUOTE_ALL)
                    temp_day = last_known_date + datetime.timedelta(days=1)
                    for x in range(0, num_days_between):
                        new_row = [temp_day, float(0), float(0), float(0), float(0), float(0), float(0)];
                        file.writerow(new_row)
                        temp_day += datetime.timedelta(days=1)
                        datafile.flush()
                    datafile.close()
                
                
        #if the file doesn't exist, create a new one with today as the start date.
        #FUTURE FIX!! - abillity to retroactively add days
        if(FileCheck("data.csv") == False):
            print "File not found. Creating..."
            data1 = ["Day/Category", "Food/Dining", "Entertainment", 
            "General Bills", "Transportation", "Cosmetics", "Miscellaneous"];
            data2 = [date.today(), float(0), float(0), float(0), float(0), float(0), float(0)];
            with open("data.csv","w") as datafile:
                out = csv.writer(datafile, delimiter=',',quoting=csv.QUOTE_ALL)
                out.writerow(data1)
                out.writerow(data2)
                datafile.flush()
            datafile.close()
            #new_file_flag = True
        data = csv.reader(open("data.csv", "rU"))
        num_cols = len(data.next())
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        #get first date in database for comparison
        first_date = data[1][0].split("-")
        first_date = date(int(first_date[0]), int(first_date[1]), int(first_date[2]))
        #category array for mapping categories to numbers
        cat_map = []
        for x in range(0, num_cols):
            cat_map.append(data[0][x])
   
        
        
def run():
    temp = budget() 