# Web-scraping only Route and Stop Information from the Unitrans website
# compiles all stops from all routes into one giant data frame for later access

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # for controlling drop-down boxes
import pandas as pd
import time


# input:
#   browser
#   r - bus line being scraped
# output: True if stops located and route is in service, False otherwise
def navigate_line(r, browser):
    route_url = "https://unitrans.ucdavis.edu/routes/" + r + "/prediction"
    browser.get(route_url)
    print("Scraping Line ", r)

    try:  # Wait until the final element is loaded.
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//select[@id='stop-select']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
        return False

    try:  # wait until page fully loaded
        WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//span[@class='time']")))
    except TimeoutException:
        print(r, "Line timed out")
        prediction_check = browser.find_element_by_xpath("//div[@class='prediction']")
        prediction_tags = prediction_check.find_elements_by_css_selector('p')
        if prediction_tags[1].get_attribute('style') == "display: none;":
            print("ROUTE NOT IN SERVICE")
            return False
    return True


def main():
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

    # initialize lists, ignore direction
    routes = list()  # will store many instances of each bus line letter, equal to the number of stops for that line
    stops = list()  # stores all stops of all bus lines
    route_letters = list()  # stores single instances of line letters
    select_route = Select(browser.find_element_by_id('route-select'))
    for r in select_route.options:  # store a list of routes
        route_letters.append(r.text)

    # TODO: scrape what kind of service there is: Day, Weekday/Weekend, etc?

    for r in route_letters:
        success = navigate_line(r, browser)
        if not success:  # only add to data frame if stops are located
            continue

        # fill in data frame
        select_stop = Select(browser.find_element_by_id('stop-select'))
        for s in select_stop.options:
            routes.append(r)
            stops.append(s.text)

    all_lines = pd.DataFrame({
        "Route": routes,
        "Stop": stops
    })

    all_lines.to_csv("stop_files/bus_stop_options.csv", encoding='utf-8', index=False)
    browser.close()
    print("Scraping finished in --- %s seconds ---" % round(time.clock() - start_time, 2))


main()