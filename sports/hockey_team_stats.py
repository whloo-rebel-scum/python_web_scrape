from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


# - scrape team stats for all 31 NHL teams
# - place them in panda dataframes for further analysis
# - https://www.hockey-reference.com/teams/


def main():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='C:\\Users\\whloo\\PycharmProjects\\chromedriver.exe',
                               chrome_options=option)

    teams_url = "https://www.hockey-reference.com/teams/"
    browser.get(teams_url)
    timeout = 20
    try:
        # Wait until the final element is loaded.
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@id='all_active_franchises']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.close()

    # generate data frame with all team names as indexes
    active_container = browser.find_element_by_id('all_active_franchises')
    rows = active_container.find_elements_by_class_name('full_table')
    team_names = list()
    for r in rows:
        team_name = r.find_element_by_css_selector('a')
        team_names.append(team_name.text)
    df = pd.DataFrame(index=team_names)

    # also gather all data in each row, append to data frame
    #   extract data from each row
    #   append to data frame

    # assign labels for columns
    row = rows[0].find_elements_by_css_selector('td')
    col_labels = list()
    for r in row:
        col_labels.append(r.get_attribute('data-stat'))
    print(col_labels)

    # df.columns = col_labels  # ValueError: Length mismatch: Expected axis has 0 elements, new values have 16 elements

    # print(df)

    # then add all other data, row by row
    browser.quit()

main()