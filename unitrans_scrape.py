# Web-Scraping on the UC Davis Unitrans website (W Line focus)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling dropdown boxes
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
select_route = Select(browser.find_element_by_id('route-select'))
print(select_route.first_selected_option.text, 'LINE STOP PREDICTIONS', '\n')
# the following lists will be put into a data frame
stops = list()  # list of names of bus stops
times = list()  # when the next bus is predicted to arrive for each stop
in_out_bound = list() # list of inbound/outbound labels for each stop

select_direction = Select(browser.find_element_by_id('direction-select'))
for d in select_direction.options[1:]:  # skip the very first option for direction
    select_direction.select_by_visible_text(d.text)  # select the direction
    select_stop = Select(browser.find_element_by_id('stop-select'))  # get local stops for that direction
    for o in select_stop.options:
        direction = re.match(r'(.*) to (.*)', d.text)  # regular expressions to shorten to Inbound/Outbound
        in_out_bound.append(direction.group(1))
        select_stop.select_by_visible_text(o.text)  # select stop
        stop = re.match(r'(.*)\((.*)', o.text)
        stops.append(stop.group(1))  # regex to remove cardinal directions
        arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
        a_t = arrival_times[0].text
        next_bus = re.match(r'(.*), (.*)?', a_t)  # regex to shorten to two
        times.append(next_bus.group(1) + 'm')

# put data into data frame
WLine = pd.DataFrame({
    "Direction": in_out_bound,
    "Stop": stops,
    "Next Bus": times
})

print(WLine)
browser.close()
