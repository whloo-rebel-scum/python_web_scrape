import re # regular expressions
import requests
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

# Browse to Rap Genius
browser = RoboBrowser(history=True)
browser.open("http://genius.com/")
# Search for Queen
form = browser.get_form(action="/search") # why doesn't this work?
form                # <RoboForm  q=>
form['q'].value = 'queen'
browser.submit_form(form)

'''
# Look up the first song
songs = browser.select('.song_name')
browser.follow_link(songs[0])
lyrics = browser.select('.lyrics')
lyrics[0].text      # \n[Intro]\nIs this the real life...

# Back to results page
browser.back()

# Look up my favorite song
browser.follow_link('death on two legs')

# Can also search HTML using regex patterns
lyrics = browser.find(class_=re.compile(r'\blyrics\b'))
lyrics.text         # \n[Verse 1]\nYou suck my blood like a leech...
'''