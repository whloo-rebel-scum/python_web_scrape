# uses the csv file created by unitrans_stop_scrape to allow the user
# to get route and stop prediction times

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import time

# read in csv file to var
lines = pd.read_csv('bus_stop_options.csv')
# print list of available lines, ask user to pick one (or quit (or show prediction times of saved stops)
print(lines['Route'].unique())  # isolate first col (Route)
route_choice = input("Choose a bus line: ")
print("Line ", route_choice, " chosen")
# also option to delete a saved stop, or all

# sort data frame according to user choice, only show stops for the chosen line
# print list of relevant stops

# retrieve prediction time
start_time = time.clock()
print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))
# ask if user would like to save the stop (Y/N)
# if yes, save to another csv file titled 'saved_stops' (write to existing one, create new one if none)

# loop until user chooses to end the program


