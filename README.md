# Web-Scraping
Using BeautifulSoup (and a ton of Google Translate !!), I was able to scrape an OTT website (HamiVideo). I also queried the imdb database for possible name matches so that further data can be collected wherever possible.
The following packages are needed to run the script:-
- Pandas
  ```
  pip install pandas #This will also install numpy and other dependencies for pandas 
  ```
- Requests
  ```
  pip install requests
  ```
- Beautiful Soup
  ```
  pip install beautifulsoup4
  ```
- Google Translator (3rd party)
  ```
  pip install googletrans
  ```
- IMdBPy (package for retrieving data from IMdB) (3rd party)
  ```
  pip install IMDbPY
  ```
- tqdm
  ```
  pip install tqdm
  ```
Run the script using
```
python hami-scraping.py
```
