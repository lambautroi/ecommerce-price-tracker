# Simple Bookstore Scraper

This is a small script I wrote to scrape book details (title, price, stock status) from a test site. It outputs everything into a CSV file. 
Good for basic price monitoring or just collecting data quickly without dealing with APIs.

## How to use

First install the requirements:
```bash
pip install -r requirements.txt
```

Then just run the script:
```bash
python scraper.py
```

By default it grabs 1 page of the science section, but you can pass arguments to scrape more:
```bash
python scraper.py --pages 3 --output my_books.csv
```

## Tools used
- python 3
- requests
- beautifulsoup4
