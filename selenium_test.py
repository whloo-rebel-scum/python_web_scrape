# Testing Selenium
from selenium import webdriver # this allows launching of the browser
from selenium.webdriver.common.by import By # enables search by parameter
from selenium.webdriver.support.ui import WebDriverWait # wait for page load
from selenium.webdriver.support import expected_conditions as EC # specify what you're looking for
from selenium.common.exceptions import TimeoutException # handling timeouts

