# Python Web Scraping
Basic tutorial: https://www.dataquest.io/blog/web-scraping-tutorial-python/

Selenium tutorial: https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72

Utilizes:
- BeautifulSoup
- Pandas data frames
- Selenium

Currently testing web scraping on weather data, from:
- https://forecast.weather.gov/MapClick.php?lat=38.54669000000007&lon=-121.74456999999995#.W1Y4ytJKjb0
- https://weather.com/weather/tenday/l/USCA0284:1:US

TODO: gather data from Unitrans Website using Selenium: https://unitrans.ucdavis.edu/routes/W/prediction
- TODO: fix prediction_scrape by scraping only one line?
- TODO: combine all bus line scripts into one program
- TODO: use phantom browser instead of Chrome?
- TODO: ignore saved stop if it isn't running at time of request

TODO: scrape sports game scores and stats, develop consistency rating?
- https://www.hockey-reference.com/
    - TODO: scrape individual team data (season to season)
- https://www.baseball-reference.com/
- https://www.pro-football-reference.com/
- https://www.basketball-reference.com/