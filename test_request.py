# Testing web scraping on weather data

import requests
import pandas as pd

from bs4 import BeautifulSoup


# page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
# page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
# page = requests.get("https://unitrans.ucdavis.edu/routes/W/prediction")
page = requests.get(
 "https://forecast.weather.gov/MapClick.php?lat=38.54669000000007&lon=-121.74456999999995#.W1Y4ytJKjb0")
soup = BeautifulSoup(page.content, 'html.parser')  # create soup object
'''
print([type(item) for item in list(soup.children)])  # get list of all soup elements
html = list(soup.children)[2]  # parse html tag
body = list(html.children)[3]  # get into body of the html tag (separated by commas)
print(list(body.children))
p = list(body.children)[1]  # isolate the p tag in the body
print(p.get_text())
'''
'''
# print(soup.find_all('p'))  # find all p tags
print(soup.find_all('p')[0].get_text())
'''
'''
print(soup.find_all(class_='inner-text'))  # find by class, html tags must come before class
# find by class needs underscore, id doesn't
print(soup.find_all(id='first'))
'''
# for CSS selectors: use double quotes, tags within tags e.g. div p means find all p within div tags
# print(soup.select("div p"))

# Weather test:
seven_day = soup.find(id="seven-day-forecast")
'''
forecast_items = seven_day.find_all(class_="forecast-tombstone")
today = forecast_items[0]
# period = today.find(class_="period-name").get_text()
# short_desc = today.find(class_="short-desc").get_text()
# temp = today.find(class_="temp").get_text()
# print(period, "\n", short_desc, "\n",  temp)
img = today.find("img")  # navigating other tags
desc = img['title']  # accessing list element
print(desc)
'''

# Weather test: extracting all information
period_tags = seven_day.select(".tombstone-container .period-name")  # periods needed for classes
periods = [pt.get_text() for pt in period_tags]
print(periods)
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d['title'] for d in seven_day.select(".tombstone-container img")]
print(short_descs)
print(temps)
print(descs)

# Using pandas dataframes
weather = pd.DataFrame({
  "desc": descs,
  "period": periods,
  "short_desc": short_descs,
  "temp": temps
})

print(weather)

# Weather test 2: Weather Channel
page = requests.get(
    "https://weather.com/weather/tenday/l/USCA0284:1:US")
soup = BeautifulSoup(page.content, 'html.parser')
ten_day = soup.find_all('td', class_="twc-sticky-col", classname="twc-sticky-col")
hilo = soup.find_all('td', class_="temp", headers="hi-lo")
# how to parse an individual element in a list?
print(hilo)
days = [d.get_text() for d in soup.find_all(class_="date-time")]
short_descs = [sd['title'] for sd in ten_day]
print(days)
print(short_descs)

weather2 = pd.DataFrame({
    "days": days,
    "short_desc": short_descs
})

print(weather2)
