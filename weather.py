#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 21:11:24 2023

@author: jackmcnamara
"""

import csv
from datetime import datetime
from operator import itemgetter

COLUMNS = ["date",  "average temp", "high temp", "low temp", "precipitation", \
           "snow", "snow depth"]

TOL = 0.02

BANNER = """This program will take in csv files with weather data and compare \
the sets.\nThe data is available for high, low, and average temperatures,\
\nprecipitation, and snow and snow depth. when prompted for a category of data, \
\nplese type one of these options: "average temp", "high temp", "low temp", \
\n"precipitation", "snow", "snow depth" """   


MENU = '''
        Menu Options:
        1. Highest value for a specific column for all cities
        2. Lowest value for a specific column for all cities
        3. Average value for a specific column for all cities
        4. Modes for a specific column for all cities
        5. Summary Statistics for a specific column for a specific city
        6. High and low averages for each category across all data
        7. Quit
        Menu Choice: '''
        
      
        
def open_files():
    ''' open multiple files from given city names, return the names of the
    cities and the files that they corespond to'''
    cities = input("Enter cities names: (comma seperated)")
    #creates city list
    city_list = cities.split(',')
    file_list = []
    valid_cities = []
    return_list = []
    # iterates through cities given by the user
    for city in city_list:
        #adds .csv to city to check for files
        city_file_name = city + '.csv'
        try:
            #tries to pen the file and adds the city to a list and file to a list
            fp = open(city_file_name)
            valid_cities.append(city)
            file_list.append(fp)
        except:
            #if the file was unabale to open the user is asked for another
            print("\nError: File {} is not found".format(city_file_name))
    return_list.append(valid_cities)
    return_list.append(file_list)
    return return_list

            
    
    
        

def read_files(cities_fp):
    '''takes a list of files and creates lists of data from the files'''
    # makes empty list for the returned list of the files info
    final_list = []
    # iterates through the files in the list of files
    for files in cities_fp:
        file_list = []
        reader = csv.reader(files)
        #skip 2 lines
        next(reader)
        next(reader)
        # iterates through the line in the file
        for line in reader:
            # list of elements in each line
            line_list = []
            for el in line:
                # as long as the element is not empty...
                if el !='':
                    # try to float the element and append to the list
                    try:
                       el = float(el)
                       line_list.append(el)
                    # if it is not floatable it is lseft as a string
                    except:
                        line_list.append(el)
                # in the case where the element is empty None is added
                else:
                    line_list.append(None)
            # converts the list of elements in each line to a tuple
            line_tup = tuple(line_list)
            # adds tuple to the list for the file
            file_list.append(line_tup)
        # adds each files list to the final list
        final_list.append(file_list)
    return final_list

                   
                   
        

def get_data_in_range(master_list, start_str, end_str):
    '''checks to see if the date of colected data is between the users 
    specified dates and returns the data if it is'''
    # creates value for dates that are comparable
    start_date = datetime.strptime(start_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(end_str, "%m/%d/%Y").date()
    # final list to append othe lists to
    final_list = []
    # iterates though the files in the master list
    for file in master_list:
        #makes a list to add tuples to
        file_list = []
        # iterates through the tuples in the list
        for tup in file:
            # makes comparable date for the tuple
            tup_date = datetime.strptime(tup[0], "%m/%d/%Y").date()
            # if the tuple date is between ore eqiual to the staer and end dates
            # the folowing suite is exicuted
            if tup_date >= start_date and tup_date <= end_date:
                file_list.append(tup)
        # adds the valid list of tuples to the 
        final_list.append(file_list)
    return final_list
        
            

def get_min(col, data, cities): 
    '''finds the min value in an input colum for a cites data and returns the 
    min with the name of the city'''
    final_list =[]
    #enumerates data for each iteration, this is so i can match the city with
    #the corect set of data
    for i,f in enumerate(data):
        list_of_vals =[]
        #goes through each tuple in the data and adds the desired value to a 
        #list as long as its value is not None
        for tup in f:
            if tup[col]!=None:
                list_of_vals.append(tup[col])
            else:
                continue
        # finds the lowest value in the list of values
        min_val = min(list_of_vals)
        # makes tuple with the city name and min val (city name is retrived 
        #through the iteration value given my the enumrate)
        cit_min = cities[i] , min_val
        # adds the tuple to the final list
        final_list.append(cit_min)
    return final_list
        
        
    
        
def get_max(col, data, cities): 
    '''finds the max value in an input colum for a cites data and returns the 
    max with the name of the city'''
    final_list =[]
    #enumerates data for each iteration, this is so i can match the city with
    #the corect set of data
    for i,f in enumerate(data):
        list_of_vals =[]
        #goes through each tuple in the data and adds the desired value to a 
        #list as long as its value is not None
        for tup in f:
            if tup[col]!=None:
                list_of_vals.append(tup[col])
            else:
                continue
        # finds the highest value in the list of values
        max_val = max(list_of_vals)
        # makes tuple with the city name and max val (city name is retrived 
        #through the iteration value given my the enumrate)
        cit_max = cities[i] , max_val
        # adds the tuple to the final list
        final_list.append(cit_max)
    return final_list


def get_average(col, data, cities): 
    '''finds the average value in an input colum for a cites data and returns the 
    max with the name of the city'''
    final_list =[]
    #enumerates data for each iteration, this is so i can match the city with
    #the corect set of data
    for i,f in enumerate(data):
        list_of_vals =[]
        #goes through each tuple in the data and adds the desired value to a 
        #list as long as its value is not None
        for tup in f:
            if tup[col]!=None:
                list_of_vals.append(tup[col])
            else:
                continue
        # fsumms all values and devides by the number of values to make an 
        # average, then rounds to 2 digits
        av_val = round((sum(list_of_vals))/(len(list_of_vals)),2)
        # makes tuple with the city name and average val (city name is retrived 
        #through the iteration value given my the enumrate)
        cit_av = cities[i] , av_val
        # adds the tuple to the final list
        final_list.append(cit_av)
    return final_list


def get_modes(col, data, cities):
    '''given data, this finds the mode (most common) value  for each city for
    a specified category of information'''
    final_list =[]
    # itteraes through and i keeps track of iteration of data
    for i,f in enumerate(data):
        list_of_vals =[]
        #goes through each tuple in the data and adds the desired value to a 
        #list as long as its value is not None
        for tup in f:
            if tup[col]!=None:
                list_of_vals.append(tup[col])
            else:
                continue
        # sorts in order of value from high to low
        list_of_vals=sorted(list_of_vals)
        list_of_streaks = []
       # for the values in list_of_vals with index tracking the iteration
        for index,val in enumerate(list_of_vals):
            # sets continue condition to true
            cont = True
            # asigns values to strak and adder origonally, streak counts how 
            # long each number is in the tolarable range
            streak = 1
            adder = 1
           # loop continues until cont == False
            while cont == True:
                # if the iteration is on the last number in list_of_vals then
                # the try is skipped and goes straight to the except
                try:
                    # adds index and adder for the value that will be subtraced 
                    # from the current streak representative
                    next_val = index+adder
                    # finds the absolute value of n1-n2/n1
                    abs_val = abs((val-list_of_vals[next_val])/val)
                    # if the value of abs_val is lees than the .02 tolarance
                    #then the streak is incresed by one and so is the index adder
                    if abs_val<TOL:
                        adder += 1
                        streak += 1
                    # if its higher than 2 the while loop is broken and the \
                    # next value is checked for its streak
                    else:
                        #makes a tuple of the streak value and the 
                        #representative of the streak
                        streak_tup = streak , val
                        list_of_streaks.append(streak_tup)
                        cont = False
                # this breaks the loop when no more vlaues are left in the list
                except:
                    streak_tup = streak , val
                    list_of_streaks.append(streak_tup)
                    cont = False
       #setting the max streak very low to compare values
        max_streak = 0
        list_of_modes = []
        for tup in list_of_streaks:
            # if the value of the streak is more than max streak...
            if tup[0]>max_streak:
                # max streaks value is replaced by the new max streak value
                max_streak = tup[0]
                # amode is th vlaue of the max sreak representative
                amode = tup[1]
        # adds amod to a list of modes
        list_of_modes.append(amode)
        for tup in list_of_streaks:
           # if there is another mode with the same streak it is  added to the 
           # list
            if tup[0] == max_streak and tup[1]!=amode:
                list_of_modes.append(tup[1])
        # if no mode exists the list of modes is empty
        if max_streak == 1:
            list_of_modes =[]
        #creates a tuple with the mode data
        cit_mod_streak = cities[i] , list_of_modes , max_streak
       # adds the tuple to the final list
        final_list.append(cit_mod_streak)
    return final_list

                    
def high_low_averages(data, cities, categories):
    '''finds the highest and lowest average for a category given by the user
    for each city given by the user'''
    list_list_of_avs = []
    #for each category...
    for cat in categories:
        try:
            # try to find the index of the category
            cat_index = COLUMNS.index(cat)
            # using the category we find the average for the data in that 
            #column
            list_of_averages = get_average(cat_index, data, cities)
            # adds average to list ofa avs
            list_list_of_avs.append(list_of_averages)
        # if the category is not valid none is added to the list of averages
        except ValueError:
            list_list_of_avs.append(None)
    
    final_list = []
    for l in list_list_of_avs:
        # sets max to very low and min to very high numbers
        max_val = 0
        min_val = 10**10
        list_list = []
        if l == None:
            # if the list is a None then it is added and continues to next 
            # itteration
            final_list.append(None)
            continue
       
        for tup in l:
            # if the value of the average is more than the max, it is now the
            # max
            if tup[1]>max_val:
                max_val = tup[1]
                max_tup = tup
            # if the value of the average is less than min, it is now the
            # min
            if tup[1]<min_val:
                min_val = tup[1]
                min_tup = tup
        # adds the max and min tups to their lists then adds both of them to 
        # the final list
        list_list.append(min_tup)
        list_list.append(max_tup)
        final_list.append(list_list)
    return final_list

          
            
        

def display_statistics(col,data, cities):
    '''displays statistics for given cities data and columns'''
    # defines the statistics for the data
    max_tup = get_max(col, data, cities)
    min_tup = get_min(col, data, cities)
    av_tup = get_average(col, data, cities)
    modes_list = get_modes(col, data, cities)
    #enumerates cities and goes through each city 
    for i,c in enumerate(cities):
        #makes mods an empty string 
        mods = ''
        for mod in modes_list[i][1]:
            # each mode in the list of modes is concatned to the string with a 
            # comma
            mods += str(mod)+','
        # removes the commas from the end of the string
        mods = mods.strip(',')
        # print city
        print(str(c) +':')
        # print max, min, and average
        print("\tMin: {:.2f} Max: {:.2f} Avg: {:.2f}".format(min_tup[i][1],\
        max_tup[i][1],av_tup[i][1]))
        if modes_list[i][2]>1: 
            # if a mode exists list it 
            print("\tMost common repeated values ({:d} occurrences): {:s}\n"\
            .format(modes_list[i][2],mods))
        #otherwise state tha no mode exists
        else:
            print('\tNo modes.')
           
            
    return

             
def main():
    print(BANNER)
    #gets cities and files ,master list form read file, and ask the user to 
    # enter an option
    cities,files = open_files()
    master_list = read_files(files)
    user_opt = int(input(MENU))
    # until the user choses o quit the loop continues
    while user_opt != 7:
        # start and end dates are made and the data between the dates is 
        # asigned to dat_in dates
        start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
        end_date = input ("\nEnter an ending date (in mm/dd/yyyy format): ")
        data_in_dates = get_data_in_range(master_list, start_date, end_date)
        # if the option is 1
        if user_opt == 1:     
            user_cat = (input("\nEnter desired category: ")).lower()
            valid = False
            while valid != True:
                try:    
                    # find the index of the categor using COLUMNS
                    col = COLUMNS.index(user_cat)
                    
                    # the loop can end if the index works becuse tha means its
                    # a valid option
                    
                    valid = True
                    
                    # finds the values and prints the users category
                    max_list = get_max(col, data_in_dates, cities)
                    print("\n\t{}: ".format(user_cat))
                    for tup in max_list:
                        # prints values
                        print("\tMax for {:s}: {:.2f}".format(tup[0],tup[1]))
                except:
                    # asks for new input
                    print("\n\t{} category is not found.".format(user_cat))
                    user_cat = (input("\nEnter desired category: ")).lower()

        elif user_opt == 2:     
            # takes a user category
            user_cat = (input("\nEnter desired category: ")).lower()
            valid = False
            while valid != True:
                try:    
                    # find the index of the categor using COLUMNS
                    col = COLUMNS.index(user_cat)
                    # the loop can end if the index works becuse tha means its
                    # a valid option
                    valid = True
                    # finds the values and prints the users category
                    min_list = get_min(col, data_in_dates, cities)
                    print("\n\t{}: ".format(user_cat))
                    for tup in min_list:
                        # prints values 
                        print("\tMin for {:s}: {:.2f}".format(tup[0],tup[1]))
                except ValueError:
                    # if the option is not in COLUMNS the the user is propt for 
                    #a new input 
                    print("\n\t{} category is not found.".format(user_cat))
                    user_cat = (input("\nEnter desired category: ")).lower()

        elif user_opt == 3:
            # takes a user category
            user_cat = (input("\nEnter desired category: ")).lower()
            valid = False
            while valid != True:
                try:    
                    # find the index of the categor using COLUMNS
                    col = COLUMNS.index(user_cat)
                    # the loop can end if the index works becuse tha means its
                    # a valid option
                    valid = True
                    # finds the values and prints the users category
                    av_list = get_average(col, data_in_dates, cities)
                    print("\n\t{}: ".format(user_cat))
                    for tup in av_list:
                        # prints values
                        print("\tAverage for {:s}: {:.2f}".format(tup[0],tup[1]))
                except ValueError:
                    # asks for new input
                    print("\n\t{} category is not found.".format(user_cat))
                    user_cat = (input("\nEnter desired category: ")).lower()

        elif user_opt == 4:
            # takes a user category
            user_cat = (input("\nEnter desired category: ")).lower()
            valid = False
            while valid != True:
                try:    
                    # find the index of the categor using COLUMNS
                    col = COLUMNS.index(user_cat)
                    # the loop can end if the index works becuse that means its
                    # a valid option
                    valid = True
                    # finds the values and prints the users category
                    mode_list = get_modes(col, data_in_dates, cities)
                    print("\n\t{}: ".format(user_cat))
                    for tup in mode_list:
                        mod_str = ''  
                        #adds each mode to a list of modes
                        for mod in tup[1]:
                           mod_str += str(mod)
                        # prints values
                        print("\tMost common repeated values for {:s} ({:d} occurrences): {:s}\n".format(tup[0],tup[2],mod_str))
                except ValueError:
                    # asks for new input
                    print("\n\t{} category is not found.".format(user_cat))
                    user_cat = (input("\nEnter desired category: ")).lower()
        
        
        elif user_opt == 5:
            user_cat = (input("\nEnter desired category: ")).lower()
            valid = False
            while valid != True:
                try:    
                    # find the index of the categor using COLUMNS
                    col = COLUMNS.index(user_cat)
                    # the loop can end if the index works becuse tha means its
                    # a valid option
                    valid = True
                    # finds the values and prints the users category
                    print(display_statistics(col, data_in_dates, cities))
                except ValueError:
                    print("\n\t{} category is not found.".format(user_cat))
                    user_cat = (input("\nEnter desired category: ")).lower()
        elif user_opt == 6:
            # takes a user category
            user_cats = input("\nEnter desired categories seperated by comma: ")
            cat_list = user_cats.split(',')
            # gets data from high_low_average
            high_lo_list = high_low_averages(data_in_dates, cities,\
                                                cat_list)
            print("\nHigh and low averages for each category across \
all data.")
            for i,list in enumerate(high_lo_list):
                if list:
                    print( "\tLowest Average: {:s} = {:.2f} Highest Average\
: {:s} = {:.2f}".format(list[0][0],list[0][1],list[1][0],list[1][1]))
                else:
                    print("{} is not a valid option".format(cat_list[i]))
            
         #user can input another option          
        user_opt = int(input(MENU))
    

if __name__ == "__main__":
    main()
                                           
