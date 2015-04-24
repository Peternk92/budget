#ToDO - Make sure you can see a list of percentages of money that you spend in each category

#CHANGE DATETIME TO STRING
#temp = today.strftime('%Y-%m-%d')
#print temp

#!/usr/bin/python




#ADD FUNCTION TO ERASE AND ADD NEW VALUE FOR A CELL



import datetime
from datetime import date
import time
import csv
import random


def FileCheck(fn):
    try:
        open(fn, "rU")
        return True
    except IOError:
        return False

class budget:
    def __init__(self):
        self.today = date.today()
        self.first_date = date.today()
        #if file exists, check last entry to see if up to date.
        #if last entry is not today, add days until today.
        if(FileCheck("data.csv") == True):
            print "Loading in file..."
            data = csv.reader(open("data.csv", "rU"))
            num_rows = sum(1 for row in data)
            data = csv.reader(open("data.csv", "rU"))
            data = list(data)
            #check last entry
            if(data[num_rows-1][0] == self.today.strftime("%Y-%m-%d")):
                print "up to date!"
            else:
                last_date_list = data[num_rows-1][0].split("-")
                #converts to year month day date (passed in as such)
                last_known_date = date(int(last_date_list[0]),int(last_date_list[1]),int(last_date_list[2]))
                num_days_between = (self.today - last_known_date).days
                with open("data.csv","a") as datafile:  
                    file = csv.writer(datafile, delimiter=',',quoting=csv.QUOTE_ALL)
                    temp_day = last_known_date + datetime.timedelta(days=1)
                    for x in range(0, num_days_between):
                        print float("{0:.2f}".format(random.uniform(0.0, 101.0)))
                        new_row = [temp_day, float("{0:.2f}".format(random.uniform(0.0, 101.0))), float("{0:.2f}".format(random.uniform(0.0, 101.0))), 
                        float("{0:.2f}".format(random.uniform(0.0, 101.0))), float("{0:.2f}".format(random.uniform(0.0, 101.0))), 
                        float("{0:.2f}".format(random.uniform(0.0, 101.0))), float("{0:.2f}".format(random.uniform(0.0, 101.0)))];
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
        self.first_date = data[1][0].split("-")
        self.first_date = date(int(self.first_date[0]), int(self.first_date[1]), int(self.first_date[2]))
        #category array for mapping categories to numbers
        self.cat_map = []
        for x in range(0, num_cols):
            self.cat_map.append(data[0][x])
    
    def Get_cat_map(self):
        return self.cat_map
        
    def Get_today(self):
        return self.today
        
    def Get_first_date(self):
        return self.first_date
        
    def Get_data(self):
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        return data
        
    def AddTo (self, add_date, cat, amt):
        date_index = (add_date - self.first_date).days + 1
        if(date_index > 0 and add_date <= self.today):
            cat_index = self.cat_map.index(cat)
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
        
    def SubFrom(self, sub_date, cat, amt):
        date_index = (sub_date - self.first_date).days + 1
        if(date_index > 0 and sub_date <= self.today):
            cat_index = self.cat_map.index(cat)
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

    def Reset_cell(self, reset_date, cat):
        date_index = (reset_date - self.first_date).days + 1
        if(date_index > 0 and reset_date <= self.today):
            cat_index = self.cat_map.index(cat)
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

    def Reset_date(self, reset_date):
        for x in range(1, len(self.cat_map)):
            self.Reset_cell(reset_date, self.cat_map[x])
            
    def Set_specific(self, reset_date, cat, value):
        date_index = (reset_date - self.first_date).days + 1
        if(date_index > 0 and reset_date <= self.today):
            cat_index = self.cat_map.index(cat)
            data = csv.reader(open("data.csv", "rU"))
            data = list(data)
            print data[date_index][cat_index]
            data[date_index][cat_index] = value
            output = csv.writer(open("data.csv", "wb"))
            x = 0
            for row in data:
                output.writerow(data[x])
                x += 1

    def Total_per_cat(self, cat):
        cat_index = self.cat_map.index(cat)
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0.0
        for x in range(1, len(data)):
            total += float(data[x][cat_index])
        return float("{0:.2f}".format(total))
    
    def Total_per_month(self, passed_date):
        #FIX: CHECK IF DATE IS IN FILE MAYBE CREATE A FUNCTION FOR CHECKING
        #FIX: CHECK IF END OF FILE
        passed_date = passed_date.strftime('%Y-%m-%d')
        month = int(passed_date.split("-")[1].lstrip("0"))
        year = passed_date.split("-")[0]
        passed_date = date(int(year), int(month), int(01))
        #print passed_date
        date_index = (passed_date - self.first_date).days + 1
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0
        current_month_from_data = month
        flag = True
        while (flag):
            temp = 0
            #print data[date_index]
            for x in range(1, len(self.cat_map)):
                temp += float(data[date_index][x])
                total += float(data[date_index][x])
            date_index += 1
            current_month_from_data = data[date_index][0].split("-")
            current_month_from_data = int(current_month_from_data[1].lstrip("0"))
            if(current_month_from_data != month):
                flag = False
        return float("{0:.2f}".format(total))
        
    def Total_per_cat_per_month(self, cat, passed_date):
        #FIX: CHECK IF DATE IS IN FILE MAYBE CREATE A FUNCTION FOR CHECKING
        #FIX: CHECK IF END OF FILE
        cat_index = self.cat_map.index(cat)
        passed_date = passed_date.strftime('%Y-%m-%d')
        month = int(passed_date.split("-")[1].lstrip("0"))
        year = passed_date.split("-")[0]
        passed_date = date(int(year), int(month), int(01))
        #print passed_date
        date_index = (passed_date - self.first_date).days + 1
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0
        current_month_from_data = month
        flag = True
        while (flag):
            #print data[date_index]
            total += float(data[date_index][cat_index])
            date_index += 1
            current_month_from_data = data[date_index][0].split("-")
            current_month_from_data = int(current_month_from_data[1].lstrip("0"))
            if(current_month_from_data != month):
                flag = False
        return float("{0:.2f}".format(total))
        
    def Percent_per_cat_per_month(self, cat, passed_date):
        temp = self.Total_per_cat_per_month(cat, passed_date) / self.Total_per_month(passed_date)
        temp = temp * 100
        return float("{0:.2f}".format(temp))


    def Average_per_cat_per_month(self, cat, passed_date):
        cat_index = self.cat_map.index(cat)
        passed_date = passed_date.strftime('%Y-%m-%d')
        month = int(passed_date.split("-")[1].lstrip("0"))
        year = passed_date.split("-")[0]
        passed_date = date(int(year), int(month), int(01))
        #print passed_date
        date_index = (passed_date - self.first_date).days + 1
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0
        count = 0
        current_month_from_data = month
        flag = True
        while (flag):
            #print data[date_index]
            total += float(data[date_index][cat_index])
            date_index += 1
            current_month_from_data = data[date_index][0].split("-")
            current_month_from_data = int(current_month_from_data[1].lstrip("0"))
            if(current_month_from_data != month):
                flag = False
            count += 1
        return float("{0:.2f}".format(total/count))
    
    def Get_date_info(self, passed_date):
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        date_index = (passed_date - self.first_date).days + 1
        return_date = []
        return_date.append(data[0])
        return_date.append(data[date_index])
        """
        line_count = 0
        for line in return_date:
            string_count = 0
            for string in line:
                temp = []
                for char in string:
                    temp.append(char)
                add_space = 16 - len(temp)
                if(line_count == 1 and string_count != 0):
                    temp.insert(0,'$')
                    add_space -= 1
                    
                if(string_count != len(return_date[line_count]) - 1):
                    temp.append(',')
                for x in range(0, add_space):
                    temp.append(' ')
                return_date[line_count][string_count] = ''.join(temp)
                #return_date[line_count] = temp_string
                #temp_string = ''
                string_count += 1
            temp_string = ''.join(return_date[line_count])
            return_date[line_count] = temp_string
            temp_string = ''
            line_count += 1
        """
        
        
        line_count = 0
        for line in return_date:
            string_count = 0
            for string in line:
                temp = []
                for char in string:
                    temp.append(char)
                add_space = 14 - len(temp)
                if(line_count == 1 and string_count != 0):
                    temp.insert(0,'$')
                    add_space -= 1
                    
                if(string_count != len(return_date[line_count]) - 1):
                    temp.append('\t')
                for x in range(0, add_space):
                    temp.append(' ')
                return_date[line_count][string_count] = ''.join(temp)
                #return_date[line_count] = temp_string
                #temp_string = ''
                string_count += 1
            temp_string = ''.join(return_date[line_count])
            return_date[line_count] = temp_string
            temp_string = ''
            line_count += 1
        
        
        
        return return_date

    def Total(self):
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0.0
        for x in range(1, len(data)):
            for y in range(1, len(self.cat_map)):
                total += float(data[x][y])
        return total

    def Percent_per_cat(self, cat):
        if(self.Total() == 0.0):
            return 0.0
        else:
            return float("{0:.2f}".format((self.Total_per_cat(cat)/self.Total()) * 100))

    def Avg_per_cat(self, cat):
        cat_index = self.cat_map.index(cat)
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        total = 0
        for x in range(1, len(data)):
            total += float(data[x][cat_index])
        total = total/(len(data)-1)
        #print float("{0:.2f}".format(total))
        return float("{0:.2f}".format(total))
        
    def print_table(self):
        data = csv.reader(open("data.csv", "rU"))
        num_cols = len(data.next())
        data = csv.reader(open("data.csv", "rU"))
        data = list(data)
        for x in range(0, len(data)):
            print ""
            for y in range(0, num_cols):
                print data[x][y] + ", ",
        print ""
    

    
        
        
#def run():
    #temp = budget()
    #temp.Percent_per_cat_per_month("Food/Dining", cal.run_cal())
    #temp.Total_per_month(cal.run_cal())
    #temp.Total_per_cat_per_month("Food/Dining", cal.run_cal())
    #tempdate = cal.run_cal()
    #category = raw_input('cat > ')
    #amount = raw_input('amt > ')
    
    #temp.AddTo(tempdate, category, float(amount))

    
#if __name__ == '__main__':
    #run()