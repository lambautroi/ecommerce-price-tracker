import requests
from bs4 import BeautifulSoup
import csv
import datetime
import argparse

def scrape_books(category_url, num_pages=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    data = []
    
    for page in range(1, num_pages + 1):
        url = category_url if page == 1 else category_url.replace("index.html", f"page-{page}.html")
        print(f"[INFO] Scraping {url}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"[ERROR] Failed to retrieve page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        
        if not books:
            break
            
        for book in books:
            title_element = book.find("h3").find("a")
            price_element = book.find("p", class_="price_color")
            availability_element = book.find("p", class_="instock availability")
            
            if title_element and price_element:
                title = title_element["title"]
                price = price_element.text.strip()
                availability = availability_element.text.strip()
                
                data.append({
                    "Title": title,
                    "Price": price,
                    "Availability": availability,
                    "Date Scraped": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
    return data

def main():
    parser = argparse.ArgumentParser(description="E-commerce Price Tracker")
    parser.add_argument("--url", type=str, default="http://books.toscrape.com/catalogue/category/books/science_22/index.html", help="Category URL to scrape")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("--output", type=str, default="output.csv", help="Output CSV file name")
    
    args = parser.parse_args()
    
    print(f"[INFO] Starting scraper for: {args.url}")
    results = scrape_books(args.url, args.pages)
    
    if results:
        keys = results[0].keys()
        with open(args.output, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
            
        print(f"[SUCCESS] Scraped {len(results)} items and saved to {args.output}")
        print("\nSample Data:")
        for i in range(min(3, len(results))):
            print(f"- {results[i]['Title']} | {results[i]['Price']}")
    else:
        print("[WARNING] No data found or scraping was blocked.")

if __name__ == "__main__":
    main()
