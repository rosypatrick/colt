"""
Colt Website Scraper

This script crawls and scrapes content from the Colt website to collect data for
our wayfinder tool demonstration.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin, urlparse
import re
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

class ColtScraper:
    def __init__(self, base_url="http://Colt.info/gb/en"):
        self.base_url = base_url
        self.visited_urls = set()
        self.data_directory = "scraped_data"
        self.products = []
        self.solutions = []
        self.technical_docs = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
    
    def clean_url(self, url):
        """Remove query parameters and fragments from URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    def is_valid_url(self, url):
        """Check if URL belongs to the Colt domain and hasn't been visited."""
        if not url:
            return False
        
        # Clean URL
        url = self.clean_url(url)
        
        # Check if already visited
        if url in self.visited_urls:
            return False
        
        # Check if it's part of the Colt domain
        parsed_url = urlparse(url)
        if "colt.info" not in parsed_url.netloc:
            return False
            
        # Skip certain file types
        if re.search(r'\.pdf$|\.jpg$|\.png$|\.gif$', parsed_url.path, re.IGNORECASE):
            # Instead of skipping PDFs entirely, capture them as technical docs
            if re.search(r'\.pdf$', parsed_url.path, re.IGNORECASE):
                self.technical_docs.append({
                    "url": url,
                    "title": os.path.basename(parsed_url.path),
                    "type": "pdf"
                })
            return False
            
        return True
    
    def extract_links(self, soup, current_url):
        """Extract all links from the page."""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href')
            full_url = urljoin(current_url, href)
            if self.is_valid_url(full_url):
                links.append(full_url)
        return links
    
    def extract_product_info(self, soup, url):
        """Extract product information from a product page."""
        try:
            # This is a placeholder - actual selectors will need to be determined
            # based on the Colt website structure
            product = {
                "url": url,
                "title": soup.title.text.strip() if soup.title else "Unknown Title",
                "description": "",
                "specifications": {},
                "images": [],
                "related_products": [],
                "categories": []
            }
            
            # Look for product description
            description_elem = soup.find("div", class_="product-description")
            if description_elem:
                product["description"] = description_elem.text.strip()
            
            # Look for specifications
            spec_elems = soup.find_all("div", class_="specification")
            for spec in spec_elems:
                key_elem = spec.find("span", class_="spec-key")
                value_elem = spec.find("span", class_="spec-value")
                if key_elem and value_elem:
                    product["specifications"][key_elem.text.strip()] = value_elem.text.strip()
            
            # Extract images
            for img in soup.find_all("img", class_="product-image"):
                if img.get("src"):
                    product["images"].append(urljoin(url, img.get("src")))
            
            self.products.append(product)
            logging.info(f"Extracted product: {product['title']}")
            
        except Exception as e:
            logging.error(f"Error extracting product info from {url}: {str(e)}")
    
    def extract_solution_info(self, soup, url):
        """Extract solution/application information."""
        try:
            # Placeholder for solution extraction logic
            solution = {
                "url": url,
                "title": soup.title.text.strip() if soup.title else "Unknown Solution",
                "description": "",
                "industries": [],
                "related_products": []
            }
            
            # Look for solution description
            description_elem = soup.find("div", class_="solution-description")
            if description_elem:
                solution["description"] = description_elem.text.strip()
            
            self.solutions.append(solution)
            logging.info(f"Extracted solution: {solution['title']}")
            
        except Exception as e:
            logging.error(f"Error extracting solution info from {url}: {str(e)}")
    
    def classify_page(self, soup, url):
        """Determine the type of page (product, solution, article, etc.)."""
        # This is a placeholder - logic will need to be customized based on Colt's site structure
        
        # Check URL patterns
        if "/products/" in url or "/product/" in url:
            return "product"
        elif "/solutions/" in url or "/applications/" in url:
            return "solution"
        elif "/technical/" in url or "/documentation/" in url:
            return "technical"
        # Add more patterns as needed
        
        # Check page content/structure if URL patterns aren't sufficient
        if soup.find("div", class_="product-details"):
            return "product"
        if soup.find("div", class_="solution-details"):
            return "solution"
        
        return "general"
    
    def process_page(self, url):
        """Process a single page - extract data and links."""
        if not self.is_valid_url(url):
            return []
        
        self.visited_urls.add(url)
        logging.info(f"Processing: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                logging.warning(f"Failed to fetch {url}: Status code {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Determine page type and extract appropriate data
            page_type = self.classify_page(soup, url)
            if page_type == "product":
                self.extract_product_info(soup, url)
            elif page_type == "solution":
                self.extract_solution_info(soup, url)
            
            # Extract links for further crawling
            return self.extract_links(soup, url)
            
        except Exception as e:
            logging.error(f"Error processing {url}: {str(e)}")
            return []
    
    def save_data(self):
        """Save the scraped data to JSON files."""
        with open(os.path.join(self.data_directory, "products.json"), "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=2)
        
        with open(os.path.join(self.data_directory, "solutions.json"), "w", encoding="utf-8") as f:
            json.dump(self.solutions, f, indent=2)
        
        with open(os.path.join(self.data_directory, "technical_docs.json"), "w", encoding="utf-8") as f:
            json.dump(self.technical_docs, f, indent=2)
        
        logging.info(f"Saved {len(self.products)} products, {len(self.solutions)} solutions, and {len(self.technical_docs)} technical documents")
    
    def crawl(self, max_pages=100):
        """Crawl the Colt website starting from the base URL."""
        to_visit = [self.base_url]
        pages_visited = 0
        
        while to_visit and pages_visited < max_pages:
            current_url = to_visit.pop(0)
            new_links = self.process_page(current_url)
            
            # Add new links to visit
            for link in new_links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
            
            pages_visited += 1
            logging.info(f"Visited {pages_visited} pages. Queue size: {len(to_visit)}")
            
            # Be respectful with crawl rate
            time.sleep(1)
        
        self.save_data()
        logging.info(f"Crawl completed. Visited {pages_visited} pages.")

if __name__ == "__main__":
    scraper = ColtScraper()
    scraper.crawl(max_pages=50)  # Adjust max_pages as needed
