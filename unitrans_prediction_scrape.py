# Web-Scraping on the UC Davis Unitrans website

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import re
import time

start_time = time.clock()

# load browser
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
browser = webdriver.Chrome(executable_path='C:\\Users\\whloo\\PycharmProjects\\chromedriver.exe',
                           chrome_options=option)
browser.get("https://unitrans.ucdavis.edu/routes/A/prediction")
timeout = 20
try:
    # Wait until the final element is loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='container']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

# examples of controlling drop-down boxes in code below
'''
# find the correct select tag
select_stop = Select(browser.find_element_by_id('stop-select'))
# select by visible text
select_stop.select_by_visible_text('Hutchison & Art Building (E)')
# select by value (Hutchison and Old Davis (E)
select_stop.select_by_value('22000')
# test print of all options
[print(o.text) for o in select_stop.options]
'''

# printing all stops with predicted arrival times
lines = list()  # list of data frames of bus routes
# the following lists will be put into data frames
stops = list()  # list of names of bus stops
times = list()  # when the next bus is predicted to arrive for each stop
in_out_bound = list()  # list of inbound/outbound labels for each stop
select_route = Select(browser.find_element_by_id('route-select'))
routes = list()
for r in select_route.options:  # store a list of routes
    routes.append(r.text)

for r in routes:
    route_url = "https://unitrans.ucdavis.edu/routes/" + r + "/prediction"
    browser.get(route_url)

    try:  # Wait until the final element is loaded.
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//select[@id='stop-select']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    print(r, 'LINE STOP PREDICTIONS:')
    select_direction = Select(browser.find_element_by_id('direction-select'))

    try:  # wait until prediction times fully loaded
        WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//span[@class='time']")))
    except TimeoutException:
        print("loading //span[@class='time'] timed out")
        prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
        prediction_tags = prediction_check.find_elements_by_css_selector('p')
        if prediction_tags[1].get_attribute('style') == "display: none;":
            print("ROUTE NOT IN SERVICE")
            continue

    # fill lists
    if len(select_direction.options) > 1:
        for d in select_direction.options[1:]:  # skip the very first direction option
            select_direction.select_by_visible_text(d.text)  # select the direction
            select_stop = Select(browser.find_element_by_id('stop-select'))  # get local stops for that direction
            for o in select_stop.options:
                direction = re.match(r'(.*) (to|and) (.*)', d.text)  # regex to shorten to Inbound or Outbound
                in_out_bound.append(direction.group(1))
                select_stop.select_by_visible_text(o.text)  # select stop
                stop = re.match(r'(.*)\((.*)', o.text)
                stops.append(stop.group(1))  # regex to remove cardinal directions
                arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
                a_t = arrival_times[0].text.split(', ')  # split by delimiter ', '
                t_str = a_t[0]
                if len(a_t) > 1:
                    t_str += ", " + a_t[1]  # have up to two bus predictions per stop
                t_str += 'm'
                times.append(t_str)
    else:  # one direction select
        select_direction.select_by_visible_text(select_direction.options[0].text)
        select_stop = Select(browser.find_element_by_id('stop-select'))
        for o in select_stop.options:
            direction = re.match(r'(.*) (to|and) (.*)',
                                 select_direction.options[0].text)
            # handle cases of inbound/outbound and clockwise/counterclockwise
            if "Both" in direction.group(1):
                in_out_bound.append("Inbound/Outbound")
            else:
                in_out_bound.append(direction.group(1))
            select_stop.select_by_visible_text(o.text)
            stop = re.match(r'(.*)\((.*)', o.text)
            stops.append(stop.group(1))
            arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
            a_t = arrival_times[0].text.split(', ')
            t_str = a_t[0]
            if len(a_t) > 1:
                t_str += ", " + a_t[1]
            t_str += 'm'
            times.append(t_str)

    # put data into data frame
    Line = pd.DataFrame({
        "Direction": in_out_bound,
        "Stop": stops,
        "Next Bus": times
    })

    print(Line, '\n')
    file_name = "bus_line_data/" + r + "_line.csv"
    Line.to_csv(file_name, encoding='utf-8', index=False)
    lines.append(Line)  # TODO: use lines var?

    # clear lists
    in_out_bound.clear()
    stops.clear()
    times.clear()
    # end loop

browser.close()
print("Scraping finished in --- %s seconds ---" % round(time.clock() - start_time, 2))
