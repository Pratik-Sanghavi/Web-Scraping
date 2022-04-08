# Web-Scraping

Two libraries for web-scraping have been explored. 
1. BeautifulSoup for scraping data off HamiVideo - a Chinese OTT platform
2. Selenium for scraping data off Booking.com

The strengths of both are reflected in the choice of web-application for each. HamiVideo doesn't have dynamically loading webpages so BeautifulSoup is perfect because it will be much faster. On the other hand, Booking.com tends to load dynamically so we need to use selenium to scroll around and click on buttons to get data exposed.
