from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pandas as pd
import csv
import time


# creates a new saved_stops.csv file
def create_saved_stops():
    routes = list()
    stops = list()
    saved_stops = pd.DataFrame({
        "Route": routes,
        "Stop": stops
    })
    saved_stops.to_csv("stop_files/saved_stops.csv", encoding='utf-8', index=False)


# returns data frame read in from saved_stops.csv
# dependent on create_saved_stops
def load_saved_stops():
    # use while loop instead to reduce number of lines?
    try:
        saved_stops = pd.read_csv('stop_files/saved_stops.csv')
        return saved_stops
    except FileNotFoundError:  # create a new saved_stops file if none exists
        create_saved_stops()
        saved_stops = pd.read_csv('stop_files/saved_stops.csv')
        return saved_stops


# add an entry to saved_stops.csv
def add_to_saved_stops(route, stop):
    # format a new row, write to the csv file
    new_stop = [route, stop]
    with open(r'stop_files/saved_stops.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(new_stop)
    print("Stop saved. Saved stops: ")
    print(load_saved_stops().to_string(index=False))


# write a data frame back to saved_stops.csv
def write_to_saved_stops(df):
    df.to_csv("stop_files/saved_stops.csv", encoding='utf-8', index=False)


# remove a stop from the csv file
# TODO: write documentation for backing out of removal
def remove_saved_stop(saved_stops):
    print(saved_stops.to_string(index=True))
    remove_choice = input("Choose a stop to remove (by index): ")
    remove_choice = remove_choice.replace(' ', '')  # eliminate whitespace
    if remove_choice == 'q':
        return
    # load data frame
    ss = load_saved_stops()
    # remove by index
    ss.drop(ss.index[int(remove_choice)], inplace=True)
    if ss.empty:
        print("Saved stops list is now empty.")
    else:
        print("New saved stops list: ")
        print(ss.to_string(index=False))
    write_to_saved_stops(ss)


# retrieve predictions for all saved stops
def saved_stop_predictions(saved_stops):
    start_time = time.clock()
    print("Saved stop predictions: \n")
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='C:\\Users\\whloo\\PycharmProjects\\chromedriver.exe',
                               chrome_options=option)
    # create lists from both columns of the data frame
    line_list = saved_stops['Route']
    stop_list = saved_stops['Stop']
    # iterate through each at the same rate
    for i in range(0, len(line_list)):
        # open predictions web page for the corresponding line and stop
        route_url = "https://unitrans.ucdavis.edu/routes/" + line_list[i] + "/prediction"
        browser.get(route_url)
        try:  # Wait until the final element is loaded.
            WebDriverWait(browser, 20).until(EC.visibility_of_element_located(
                (By.XPATH, "//select[@id='stop-select']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        # retrieve prediction, and print it
        select_stop = Select(browser.find_element_by_id('stop-select'))
        select_stop.select_by_visible_text(stop_list[i])
        try:
            WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//span[@class='time']")))
            arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
            print(line_list[i], " Line: '", stop_list[i], "' stop: ")
            print("The next bus(es) will arrive in:", arrival_times[0].text, "min\n")
        except TimeoutException:
            prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
            prediction_tags = prediction_check.find_elements_by_css_selector('p')
            if prediction_tags[1].get_attribute('style') == "display: none;":
                print("Line stopped running.\n")

    browser.close()
    print("Retrieved prediction in --- %s seconds ---" % round(time.clock() - start_time, 2))