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

def active_franchise_scrape(browser):
    start_time = time.clock()

    # generate gather team names and data from each row
    active_container = browser.find_element_by_id('all_active_franchises')
    rows = active_container.find_elements_by_class_name('full_table')
    team_names = list()
    stat_list = list()  # should be a list of lists
    for r in rows:  # TODO: simplify loop?
        team_name = r.find_element_by_css_selector('a')
        team_names.append(team_name.text)
        print(team_name.text, ": ")
        web_e_stat_list = list()
        for s in r.find_elements_by_css_selector('td'):
            web_e_stat_list.append(s.text)
        print(web_e_stat_list)
        stat_list.append(web_e_stat_list)

    # assign labels for columns
    row = rows[0].find_elements_by_css_selector('td')
    col_labels = list()
    for r in row:
        col_labels.append(r.get_attribute('data-stat'))
    print(col_labels)

    # mark time
    print("Scraped in --- %s seconds ---" % round(time.clock() - start_time, 2))

    # create data frame, inserting all elements at once
    df = pd.DataFrame(stat_list, columns=col_labels, index=team_names)
    df.to_csv("hockey_data/all_active_franchise_data.csv", encoding='utf-8')


def defunct_franchise_scrape(browser):
    start_time = time.clock()

    # generate gather team names and data from each row
    active_container = browser.find_element_by_id('all_defunct_franchises')
    rows = active_container.find_elements_by_class_name('full_table')
    team_names = list()
    stat_list = list()  # should be a list of lists
    for r in rows:  # TODO: simplify loop?
        team_name = r.find_element_by_css_selector('a')
        team_names.append(team_name.text)
        print(team_name.text, ": ")
        web_e_stat_list = list()
        for s in r.find_elements_by_css_selector('td'):
            web_e_stat_list.append(s.text)
        print(web_e_stat_list)
        stat_list.append(web_e_stat_list)

    # assign labels for columns
    row = rows[0].find_elements_by_css_selector('td')
    col_labels = list()
    for r in row:
        col_labels.append(r.get_attribute('data-stat'))
    print(col_labels)

    # mark time
    print("Scraped in --- %s seconds ---" % round(time.clock() - start_time, 2))

    # create data frame, inserting all elements at once
    df = pd.DataFrame(stat_list, columns=col_labels, index=team_names)
    df.to_csv("hockey_data/all_defunct_franchise_data.csv", encoding='utf-8')


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

    active_franchise_scrape(browser)
    defunct_franchise_scrape(browser)
    browser.quit()

main()