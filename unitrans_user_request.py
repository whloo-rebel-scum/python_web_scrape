# uses the csv file created by unitrans_stop_scrape to allow the user
# to get route and stop prediction times

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import time

# read in csv file to var
lines = pd.read_csv('bus_stop_options.csv')
# print list of available lines, ask user to pick one (or quit (or show prediction times of saved stops)
unique_lines = lines['Route'].unique()
print("Running lines: ", unique_lines)  # isolate first col (Route)
while True:  # TODO: implement options (quitting, etc)
    route_choice = input("Choose a bus line: ")
    if route_choice in unique_lines:
        break
    else:
        print("Invalid route.")
print("Line ", route_choice, " chosen")
print("Stops for Line ", route_choice)  # print list of relevant stops
stops = (lines[lines.Route == route_choice])['Stop']
print(stops)

while True:  # loop until successful stop selection
    stop_choice_string = "Choose a stop for the " + route_choice + " Line (enter index): "
    stop_choice = input(stop_choice_string)  # choice should be a number (index)
    # retrieve prediction time; load browser
    start_time = time.clock()
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='C:\\Users\\whloo\\PycharmProjects\\chromedriver.exe',
                               chrome_options=option)
    route_url = "https://unitrans.ucdavis.edu/routes/" + route_choice + "/prediction"
    browser.get(route_url)
    timeout = 20
    try:
        # Wait until the final element is loaded.
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='container']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    select_direction = Select(browser.find_element_by_id('direction-select'))
    select_stop = Select(browser.find_element_by_id('stop-select'))
    try:  # implement error checking for incorrect indexing
        select_stop.select_by_visible_text(lines.Stop[int(stop_choice)])
        break
    except NoSuchElementException:
        print("Invalid stop selection.")
        browser.close()
        continue

arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
print("For the '", lines.Stop[int(stop_choice)], "' stop: ")
print("The next bus(es) will arrive in:", arrival_times[0].text, "min")
browser.close()
print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))

# ask if user would like to save the stop (Y/N)
# if yes, save to another csv file titled 'saved_stops' (write to existing one, create new one if none)

# loop until user chooses to end the program


