# uses the csv file created by unitrans_stop_scrape to allow the user
# to get route and stop prediction times

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

from unitrans.saved_stop_functions import load_saved_stops
from unitrans.saved_stop_functions import add_to_saved_stops
from unitrans.saved_stop_functions import remove_saved_stop
from unitrans.saved_stop_functions import saved_stop_predictions


# input:
#   route_choice
#   stops - data frame of all stops for a given route_choice
# output: returns index from lines when successful
# Prompts the user to enter the the desired stop via data frame index.
# A correct entry causes the browser to open, navigating to the correct stop page
def stop_selection(route_choice, stops):
    while True:
        stop_choice_string = "Choose a stop for the " + route_choice + " Line (enter index): "
        stop_choice = input(stop_choice_string)  # choice should be a number (index)
        stop_choice = stop_choice.replace(' ', '')  # eliminate whitespace
        if stop_choice == 'q':  # quit program
            print("Stop selection halted.")
            return stop_choice
        elif stop_choice == 'o':  # show options
            print("OPTIONS:")
            print("Enter 'q' to halt stop selection and return to line selection.")
            print("Enter 'p' to print stops for the ", route_choice, " Line again.")
        elif stop_choice == 'p':  # print lines again
            print(stops.to_string(index=True))
        else:
            return stop_choice


# input:
#   stop_choice
#   lines - data frame of all running lines and their bus stops
# Opens browser and locates prediction times on Unitrans web page. If prediction times not located,
# it declares the line inactive. Returns True or False, indicating if retrieval was successful
def prediction_retrieval(route_choice, stop_choice, lines):
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
        browser.close()
        return False

    # how to handle this in another function?
    select_stop = Select(browser.find_element_by_id('stop-select'))
    try:  # implement error checking for incorrect indexing
        select_stop.select_by_visible_text(lines.Stop[int(stop_choice)])
    except NoSuchElementException:
        print("Invalid stop selection.")
        browser.close()
        return False

    try:
        WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//span[@class='time']")))

        # print prediction information
        arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
        print("For the '", lines.Stop[int(stop_choice)], "' stop: ")
        print("The next bus(es) will arrive in:", arrival_times[0].text, "min")
        browser.quit()
        print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))
    except TimeoutException:
        prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
        prediction_tags = prediction_check.find_elements_by_css_selector('p')
        if prediction_tags[1].get_attribute('style') == "display: none;":
            print("Line stopped running.")
            browser.close()
    return True


# input:
#   route_choice, stop_choice, lines
# Asks user if they would like to save the selected stop.
# Save if 'yes', checking if the stop already exists in the list.
def save_prompt(route_choice, stop_choice, lines):
    while True:
        save_choice = input("Would you like to save this stop (Y/N)? ")
        save_choice = save_choice.replace(' ', '')  # eliminate whitespace
        if save_choice == 'Y' or save_choice == 'y':
            # check that route and stop are on the same line
            ss = load_saved_stops()
            if ((ss['Route'] == route_choice) & (ss['Stop'] == lines.Stop[int(stop_choice)])).any():
                print("Stop already saved.")
            else:
                add_to_saved_stops(route_choice, lines.Stop[int(stop_choice)])
            break
        elif save_choice == 'N' or save_choice == 'n':
            print("Stop not saved.")
            break
        else:
            print("Invalid selection, try again.")
            continue


def main():

    lines = pd.read_csv('stop_files/bus_stop_options.csv')
    print("***enter 'o' to show additional options for user input")
    print("***enter 'q' at any input to exit the program***")
    unique_lines = lines['Route'].unique()  # isolate first col (Route)
    print("Running lines: ", unique_lines)  # print list of available lines, ask user to pick one

    while True:
        saved_stops = load_saved_stops()  # initializes, and also refreshes after removal of stop
        route_choice = input("Choose a bus line: ")
        route_choice = route_choice.replace(' ', '')  # eliminate whitespace
        if route_choice in unique_lines:  # execute main input and retrieval
            print("Line ", route_choice, " chosen")
            print("Stops for Line ", route_choice)  # print list of relevant stops
            stops = (lines[lines.Route == route_choice])['Stop']
            print(stops.to_string(index=True))

            while True:
                stop_choice = stop_selection(route_choice, stops)
                if stop_choice == 'q':
                    break
                if prediction_retrieval(route_choice, stop_choice, lines):  # return true if successful retrieval
                    break
            if stop_choice == 'q':
                continue

            save_prompt(route_choice, stop_choice, lines)

        elif route_choice == 'q' or route_choice == 'exit':  # quit program
            print("Ending program . . .")
            exit()
        elif route_choice == 'o':  # options
            print("***enter 's' at line selection to show saved stops***")
            print("***enter 'r' at line selection to remove a saved stop")
            print("***enter 'p' at line selection to print running lines again")
            print("***enter 'pr' at line selection to get prediction times for saved stops")
        elif route_choice == 'p':  # print running lines again
            print("Running lines: ", unique_lines)
        # all but one statement below require a saved_stop.empty check
        elif route_choice == 's':  # print saved stops
            if saved_stops.empty:
                print("No saved stops.")
            else:
                print("Saved stops: ")
                print(saved_stops.to_string(index=False))
        elif route_choice == 'r':  # remove a saved stop
            if saved_stops.empty:
                print("No saved stops.")
            else:
                remove_saved_stop(saved_stops)
        elif route_choice == 'pr':  # get predictions for saved stops
            if saved_stops.empty:
                print("No saved stops.")
            else:
                saved_stop_predictions(saved_stops)
        else:
            print("Invalid choice.")


main()

