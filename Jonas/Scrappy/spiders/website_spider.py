import re
import tldextract
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WebsiteSpider(CrawlSpider):
    name = "website_spider"
    scraped_data = []

    def __init__(self, start_urls, scrape_subdomains, data_to_scrape, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.scrape_subdomains = scrape_subdomains
        self.data_to_scrape = data_to_scrape

        # Extract the domain and subdomain from the start URL
        ext = tldextract.extract(start_urls[0])
        domain = f"{ext.domain}.{ext.suffix}"
        subdomain = ext.subdomain if ext.subdomain else ""

        # Set allowed domains based on the extracted domain and subdomain
        if self.scrape_subdomains:
            self.allowed_domains = [f"*{domain}"]
        else:
            self.allowed_domains = [f"{subdomain}{domain}"]

        self.rules = [
            Rule(LinkExtractor(allow=self.allowed_domains), callback="parse_item", follow=True),
        ]

    def parse_item(self, response):
        item = {}
        if "Product Names" in self.data_to_scrape:
            item["Product Name"] = response.css("h1::text").get()
        if "Product Descriptions" in self.data_to_scrape:
            item["Product Description"] = " ".join(response.css(".product-description ::text").getall())
        if "Product Prices" in self.data_to_scrape:
            item["Product Price"] = response.css(".product-price::text").get()
        if "Product Images" in self.data_to_scrape:
            item["Product Image"] = response.css(".product-image::attr(src)").get()
        if "Product Categories" in self.data_to_scrape:
            item["Product Categories"] = response.css(".product-categories a::text").getall()
        if "Product SKUs" in self.data_to_scrape:
            item["Product SKU"] = response.css(".product-sku::text").get()
        if "Product Reviews" in self.data_to_scrape:
            item["Product Reviews"] = response.css(".product-review-text::text").getall()

        if any(item.values()):
            self.scraped_data.append(item)
            yield item