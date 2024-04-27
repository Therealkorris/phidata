# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd

class ProductScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.product_data = []

    def scrape_products(self):
        self.crawl(self.base_url)
        product_df = pd.DataFrame(self.product_data, columns=['Product Name', 'Product ID', 'Price'])
        return product_df

    def crawl(self, url):
        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return

        self.visited_urls.add(url)

        # Extract product information from the page
        product_name = soup.find('h1', {'class': 'product-name'})
        product_id = soup.find('span', {'class': 'product-id'})
        price = soup.find('span', {'class': 'product-price'})

        if product_name and product_id and price:
            self.product_data.append([product_name.text.strip(), product_id.text.strip(), price.text.strip()])

        # Find links to other pages and crawl them
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and self.domain in href:
                next_url = urljoin(self.base_url, href)
                self.crawl(next_url)