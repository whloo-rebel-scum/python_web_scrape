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

from saved_stop_functions import load_saved_stops
from saved_stop_functions import add_to_saved_stops
from saved_stop_functions import remove_saved_stop
from saved_stop_functions import saved_stop_predictions

saved_stops = load_saved_stops()  # utilized in while loop
lines = pd.read_csv('bus_stop_options.csv')
print("***enter 'o' to show additional options")
print("***enter 'q' at any input to exit the program***")
unique_lines = lines['Route'].unique()  # isolate first col (Route)
print("Running lines: ", unique_lines)  # print list of available lines, ask user to pick one

while True:
    route_choice = input("Choose a bus line: ")
    route_choice = route_choice.replace(' ', '')  # eliminate whitespace
    if route_choice in unique_lines:
        break
    elif route_choice == 'q':  # quit program
        print("Good-bye!")
        exit()
    elif route_choice == 'o':  # options
        print("***enter 's' at line selection to show saved stops***")
        print("***enter 'r' at line selection to remove a saved stop")
        print("***enter 'p' at line selection to get prediction times for saved stops")
    elif saved_stops.empty:  # the statements below all require checking if saved_stops is empty
        print("No saved stops.")
    elif route_choice == 's':  # print saved stops
        print("Saved stops: ")
        print(saved_stops.to_string(index=False))
    elif route_choice == 'r':  # remove a saved stop
        remove_saved_stop(saved_stops)
        saved_stops = load_saved_stops()  # refresh saved_stops
    elif route_choice == 'p':  # get predictions for saved stops
        saved_stop_predictions(saved_stops)
    else:
        print("Invalid choice.")


print("Line ", route_choice, " chosen")
print("Stops for Line ", route_choice)  # print list of relevant stops
stops = (lines[lines.Route == route_choice])['Stop']
print(stops.to_string(index=True))

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

try:
    WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
        (By.XPATH, "//span[@class='time']")))

    # print prediction information
    arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
    print("For the '", lines.Stop[int(stop_choice)], "' stop: ")
    print("The next bus(es) will arrive in:", arrival_times[0].text, "min")
    browser.close()
    print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))
except TimeoutException:
    prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
    prediction_tags = prediction_check.find_elements_by_css_selector('p')
    if prediction_tags[1].get_attribute('style') == "display: none;":
        print("Line stopped running.")

'''
arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
print("For the '", lines.Stop[int(stop_choice)], "' stop: ")
print("The next bus(es) will arrive in:", arrival_times[0].text, "min")
browser.close()
print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))
'''

save_choice = input("Would you like to save this stop (Y/N)? ")
save_choice = save_choice.replace(' ', '')  # eliminate whitespace
if save_choice == 'Y' or save_choice == 'y':
    # check that route and stop are on the same line
    ss = load_saved_stops()
    if ((ss['Route'] == route_choice) & (ss['Stop'] == lines.Stop[int(stop_choice)])).any():
        print("Stop already saved.")
    else:
        add_to_saved_stops(route_choice, lines.Stop[int(stop_choice)])
elif save_choice == 'N' or save_choice == 'n':
    print("Stop not saved. Ending program ...")