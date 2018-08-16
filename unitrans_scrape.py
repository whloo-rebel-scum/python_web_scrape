# Web-Scraping on the UC Davis Unitrans website (W Line)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select # for controlling dropdown boxes
import pandas as pd

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

arrival_times = browser.find_elements_by_xpath("//span[@class='time']")
a_t = arrival_times[0].text
print('W LINE ARRIVAL TIMES', '\n')
print('SILO AND CENTER ISLAND (E): ', a_t, '\n')

# find the correct select tag
select_stop = Select(browser.find_element_by_id('stop-select'))
# select by visible text
select_stop.select_by_visible_text('Hutchison & Art Building (E)')
# select by value (Hutchison and Old Davis (E)
select_stop.select_by_value('22000')
# test print of all options
[print(o.text) for o in select_stop.options]
browser.close()




