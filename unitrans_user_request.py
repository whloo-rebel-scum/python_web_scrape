# uses the csv file created by unitrans_stop_scrape to allow the user
# to get route and stop prediction times

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import re
import time

start_time = time.clock()

# read in csv file to var
# print list of available lines, ask user to pick one (or quit (or show prediction times of saved stops)
# print list of available stops from the chosen line, ask user to pick one
# retrieve prediction time
# ask if user would like to save the stop (Y/N)
# if yes, save to another csv file titled 'saved_stops'

# loop until user chooses to end the program

print("Scraping finished in --- %s seconds ---" % round(time.clock() - start_time, 2))
