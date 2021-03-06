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

today = date.today()
first_date = date.today()
new_file_flag = False

def FileCheck(fn):
    try:
        open(fn, "rU")
        return True
    except IOError:
        return False
        
def AddTo (add_date, cat, amt):
    date_index = (add_date - first_date).days + 1
    if(date_index > 0 and add_date <= today):
        cat_index = cat_map.index(cat)
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        data[date_index][cat_index] = float(data[date_index][cat_index]) + float(amt)
        data[date_index][cat_index] = float("{0:.2f}".format(data[date_index][cat_index]))
        with open("data.csv", "wb") as datafile:
            output = csv.writer(datafile)
            x = 0
            for row in data:
                output.writerow(data[x])
                datafile.flush()
                x += 1
            datafile.close()
    else:
        print "date not in list"
        #insert date into file before first date and update first date variable
        return True
    return True
    
def SubFrom(sub_date, cat, amt):
    date_index = (sub_date - first_date).days + 1
    if(date_index > 0 and sub_date <= today):
        cat_index = cat_map.index(cat)
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        if(float(data[date_index][cat_index]) - float(amt) >= 0):
            data[date_index][cat_index] = float(data[date_index][cat_index]) - float(amt)
            data[date_index][cat_index] = float("{0:.2f}".format(data[date_index][cat_index]))
            with open("data.csv", "wb") as datafile:
                output = csv.writer(datafile)
                x = 0
                for row in data:
                    output.writerow(data[x])
                    datafile.flush()
                    x += 1
                datafile.close()
        else:
            print "subtraction too large"
    else:
        print "date not in list"
        #insert date into file before first date and update first date variable
        return True
    return True

def ResetCell(reset_date, cat):
    print "test1"
    date_index = (reset_date - first_date).days + 1
    if(date_index > 0 and reset_date <= today):
        print "test2"
        cat_index = cat_map.index(cat)
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        print data[date_index][cat_index]
        data[date_index][cat_index] = 0.0
        output = csv.writer(open("data.csv", "wb"))
        x = 0
        for row in data:
            output.writerow(data[x])
            x += 1
    else:
        print "date not in list"
        #insert date into file before first date and update first date variable
        return True
    return True

def ResetDate(reset_date):
    for x in range(1, len(cat_map)):
        ResetCell(reset_date, cat_map[x])

def Total_per_cat(cat):
    cat_index = cat_map.index(cat)
    data = csv.reader(open("data.csv", "rU"))
    data = list(data)
    total = 0.0
    for x in range(1, len(data)):
        total += float(data[x][cat_index])
    return float("{0:.2f}".format(total))

def Total():
    data = csv.reader(open("data.csv", "rU"))
    data = list(data)
    total = 0.0
    for x in range(1, len(data)):
        for y in range(1, len(cat_map)):
            total += float(data[x][y])
    return total
    
    
def Percent_per_cat(cat):
    if(Total() == 0.0):
        return 0.0
    else:
        return float("{0:.2f}".format((Total_per_cat(cat)/Total()) * 100))

def Avg_per_cat(cat):
    cat_index = cat_map.index(cat)
    data = csv.reader(open("data.csv", "rU"))
    data = list(data)
    total = 0
    for x in range(1, len(data)):
        total += float(data[x][cat_index])
    total = total/(len(data)-1)
    print float("{0:.2f}".format(total))
    return float("{0:.2f}".format(total))


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



#AddTo(date, category, amount)
#   adds amount to the category on date
#SubFrom(date, category, amount)
#   subtracts amonut from the category on date
#ResetCell(date, category)
#   resets category to 0.0 on date
#ResetDate(date)
#   resets all categories to 0.0 on date
#Total_per_cat(category)
#   returns the total amount from the category on all dates
#Total()
#   returns the total amount from all categories on all dates
#Percent_per_cat(category)
#   returns the percentage of the category relative to the total
#Avg_per_cat(category)
#   returns the average of the category per day


#testing    
data = csv.reader(open("data.csv", "rU"))
data = list(data)
for x in range(0, len(data)):
    print ""
    for y in range(0, num_cols):
        print data[x][y] + ", ",
print ""

Total()
Percent_per_cat("Entertainment")

action = raw_input('> ')
action = action.split()

tempdate = date(2015, 04, 19)

if(action[0].lower() == "add"):
    tempdate = cal.run_cal()
    category = raw_input('cat > ')
    amount = raw_input('amt > ')
    
    AddTo(tempdate, category, float(amount))
    
if(action[0].lower() == "sub"):
    tempdate = cal.run_cal()
    category = raw_input('cat > ')
    amount = raw_input('amt > ')
    
    SubFrom(tempdate, category, float(amount))
    
if(action[0].lower() == "reset"):
    ResetCell(tempdate, "Entertainment")

if(action[0].lower() == "resetdate"):
    ResetDate(date(2015, 04, 12))

if(action[0].lower() == "test"):
    print cal.run_cal()
if(action[0].lower() == "total"):
    Total_per_cat(action[1])
    
if(action[0].lower() == "avg"):
    Avg_per_cat(action[1])
    
data = csv.reader(open("data.csv", "rU"))
data = list(data)
for x in range(0, len(data)):
    print ""
    for y in range(0, num_cols):
        print data[x][y] + ", ",
print ""
    
action = raw_input('> ')
action = action.split()

tempdate = date(2015, 04, 19)

if(action[0].lower() == "add"):
    tempdate = cal.run_cal()
    category = raw_input('cat > ')
    amount = raw_input('amt > ')
    
    AddTo(tempdate, category, float(amount))
    
if(action[0].lower() == "sub"):
    tempdate = cal.run_cal()
    category = raw_input('cat > ')
    amount = raw_input('amt > ')
    
    SubFrom(tempdate, category, float(amount))
    
if(action[0].lower() == "reset"):
    tempdate = cal.run_cal()
    category = raw_input('cat > ')
    ResetCell(tempdate, category)

if(action[0].lower() == "resetdate"):
    ResetDate(date(2015, 04, 12))

if(action[0].lower() == "test"):
    print cal.run_cal()
if(action[0].lower() == "total"):
    Total_per_cat(action[1])
    
if(action[0].lower() == "avg"):
    Avg_per_cat(action[1])
    
data = csv.reader(open("data.csv", "rU"))
data = list(data)
for x in range(0, len(data)):
    print ""
    for y in range(0, num_cols):
        print data[x][y] + ", ",
print ""
    