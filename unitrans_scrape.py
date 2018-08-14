# Web-Scraping on the UC Davis Unitrans website (W Line)

import mechanicalsoup
import requests

from bs4 import BeautifulSoup


# Connect to duckduckgo
# browser = mechanicalsoup.StatefulBrowser()
'''
browser.open("https://duckduckgo.com/")
browser.select_form('#search_form_homepage')
browser["q"] = "MechanicalSoup"
browser.submit_selected()

for link in browser.get_current_page().select('a.result__a'):
    print(link.text, '->', link.attrs['href'])
'''
# browser.open("https://unitrans.ucdavis.edu/routes/W/prediction")
# browser.select_form('form[id="arrival-form"]')

url = 'https://unitrans.ucdavis.edu/routes/W/prediction'

'''
with requests.Session() as session:
    response = session.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    print(soup.find_all(class_='time'))
'''

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.find_all('option'))
print(soup.find_all('p', id="prediction-notice"))




