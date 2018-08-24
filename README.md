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
- COMPLETED: scraping of W-Line, data frame input, parsing with regex
- In-progress: expand to all lines, store in a list of data frames
    - TODO: optimize to only store stops and directions, for later usage and user interaction
- NEXT: scrape sports game scores