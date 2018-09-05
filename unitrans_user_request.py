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

from saved_stop_functions import load_saved_stops
from saved_stop_functions import add_to_saved_stops
from saved_stop_functions import write_to_saved_stops

# TODO: implement getting predictions for saved stops (need to add another column)
# create a new saved_stops file if none exists
saved_stops = load_saved_stops()  # data frame with all saved stops TODO: get rid of this?

# print list of available lines, ask user to pick one
lines = pd.read_csv('bus_stop_options.csv')  # read in csv file to var
print("***NOTE: enter 'q' at any input to exit the program***")
print("***enter 's' at line selection to show saved stops***")
unique_lines = lines['Route'].unique()
print("Running lines: ", unique_lines)  # isolate first col (Route)
while True:
    route_choice = input("Choose a bus line: ")
    route_choice = route_choice.replace(' ', '')  # eliminate whitespace
    if route_choice in unique_lines:
        break
    elif route_choice == 'q':  # quit program
        print("Good-bye!")
        exit()
    elif route_choice == 's':  # saved stop options
        if saved_stops.empty:
            print("No saved stops.")
        else:
            print("Saved stops: ")
            print(saved_stops.to_string(index=False))
    elif route_choice == 'r':  # remove a saved stop
        # TODO: add remove saved route option
        if saved_stops.empty:
            print("No saved stops.")
        else:
            print(saved_stops.to_string(index=True))
            remove_choice = input("Choose a stop to remove (by index): ")
            remove_choice = remove_choice.replace(' ', '')  # eliminate whitespace
            # load data frame
            ss = load_saved_stops()
            # remove by index ( df.drop(df.index[0], inplace=True) )
            ss.drop(ss.index[int(remove_choice)], inplace=True)
            print("New saved stops list: ")
            print(ss.to_string(index=False))
            write_to_saved_stops(ss)
    else:
        print("Invalid choice.")

print("Line ", route_choice, " chosen")
print("Stops for Line ", route_choice)  # print list of relevant stops
stops = (lines[lines.Route == route_choice])['Stop']
print(stops.to_string(index=True))
# TODO: how to suppress 'Name: Stop, dtype: object' printing

while True:  # loop until successful stop selection
    stop_choice_string = "Choose a stop for the " + route_choice + " Line (enter index): "
    stop_choice = input(stop_choice_string)  # choice should be a number (index)
    stop_choice = stop_choice.replace(' ', '')  # eliminate whitespace
    if stop_choice == 'q':  # quit program
        print("Good-bye!")
        exit()
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

save_choice = input("Would you like to save this stop (Y/N)? ")
save_choice = save_choice.replace(' ', '')  # eliminate whitespace
if save_choice == 'Y' or save_choice == 'y':
    # TODO: check if stop already exists in saved
    add_to_saved_stops(route_choice, lines.Stop[int(stop_choice)])
elif save_choice == 'N' or save_choice == 'n':
    print("Stop not saved. Ending program ...")