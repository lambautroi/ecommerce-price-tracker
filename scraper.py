import requests
from bs4 import BeautifulSoup
import csv
import datetime
import argparse

def get_books(url, pages=1):
    # standard user agent so we don't get blocked immediately
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"
    }
    
    results = []
    
    for p in range(1, pages + 1):
        # handling pagination
        current_url = url if p == 1 else url.replace("index.html", f"page-{p}.html")
        print(f"getting data from {current_url}...")
        
        resp = requests.get(current_url, headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code != 200:
            print(f"bad response: {resp.status_code}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")
        
        if len(items) == 0:
            break
            
        for item in items:
            title_tag = item.find("h3").find("a")
            price_tag = item.find("p", class_="price_color")
            stock_tag = item.find("p", class_="instock availability")
            
            if title_tag and price_tag:
                results.append({
                    "title": title_tag["title"],
                    "price": price_tag.text.strip(),
                    "stock": stock_tag.text.strip(),
                    "scraped_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://books.toscrape.com/catalogue/category/books/science_22/index.html")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--output", default="output.csv")
    args = parser.parse_args()
    
    data = get_books(args.url, args.pages)
    
    if data:
        # save to csv
        with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            
        print(f"done! saved {len(data)} items to {args.output}")
    else:
        print("nothing found.")
