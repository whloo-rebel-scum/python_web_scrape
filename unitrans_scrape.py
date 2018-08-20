# Web-Scraping on the UC Davis Unitrans website

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  # to handle in try-except blocks
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import re

option = webdriver.ChromeOptions()
option.add_argument("--incognito")
browser = webdriver.Chrome(executable_path='C:\\Users\\whloo\\PycharmProjects\\chromedriver.exe',
                           chrome_options=option)
browser.get("https://unitrans.ucdavis.edu/routes/W/prediction")
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
select_route = Select(browser.find_element_by_id('route-select'))
for r in select_route.options:
    select_route.select_by_visible_text(r.text)  # select route
    print(r.text, 'LINE STOP PREDICTIONS:')
    # the following lists will be put into data frames
    stops = list()  # list of names of bus stops
    times = list()  # when the next bus is predicted to arrive for each stop
    in_out_bound = list()  # list of inbound/outbound labels for each stop
    select_direction = Select(browser.find_element_by_id('direction-select'))

    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//div[@class='prediction']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    # TODO: skipping non-service line almost works, why does it a skip a few viable lines?
    browser.implicitly_wait(5)
    prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
    prediction_tags = prediction_check.find_elements_by_css_selector('p')
    if prediction_tags[1].get_attribute('style') == "display: none;":  # not in service
        print("ROUTE NOT IN SERVICE")
        continue

    # TODO: deal with F, P, Q line having only one direction option

    for d in select_direction.options[1:]:  # skip the very first option for direction
        # TODO: fix "Message: Could not locate element with visible text: Outbound to Wake Forest"
        # TODO: fix "Message: stale element reference: element is not attached to the page document"
        select_direction.select_by_visible_text(d.text)  # select the direction
        select_stop = Select(browser.find_element_by_id('stop-select'))  # get local stops for that direction
        for o in select_stop.options:
            direction = re.match(r'(.*) (to|and) (.*)', d.text)  # regular expressions to shorten to Inbound/Outbound
            in_out_bound.append(direction.group(1))
            select_stop.select_by_visible_text(o.text)  # select stop
            stop = re.match(r'(.*)\((.*)', o.text)
            stops.append(stop.group(1))  # regex to remove cardinal directions
            arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
            a_t = arrival_times[0].text
            # next_bus = re.match(r'(.*)(,?)(.*)', a_t)  # TODO regex to shorten to two
            # check if there are no more buses for the day
            # if next_bus.group(1) != "":
            #    times.append(next_bus.group(1) + 'm')
            # else:
            #    times.append('no buses')
            times.append(a_t + 'm')

    # put data into data frame
    Line = pd.DataFrame({
        "Direction": in_out_bound,
        "Stop": stops,
        "Next Bus": times
    })

    print(Line)
    lines.append(Line)
    # end loop

browser.close()
