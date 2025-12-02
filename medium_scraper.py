import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import re
from datetime import datetime

class MediumScraper:
    def __init__(self, input_csv='url_technology.csv', output_csv='scrapping_results.csv'):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.checkpoint_interval = 3
        self.driver = None
        
    def setup_driver(self):
        """Initialize undetected Chrome driver"""
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # Uncomment to run headless (faster but harder to debug)
        # options.add_argument('--headless')
        
        self.driver = uc.Chrome(options=options)
        self.driver.set_page_load_timeout(30)
        
    def get_scraped_urls(self):
        """Get list of already scraped URLs to skip"""
        if os.path.exists(self.output_csv):
            try:
                df = pd.read_csv(self.output_csv)
                return set(df['url'].tolist())
            except:
                return set()
        return set()
    
    def extract_data(self, url):
        """Extract all required data from a Medium article"""
        data = {
            'url': url,
            'title': '',
            'subtitle': '',
            'text': '',
            'no_of_images': 0,
            'image_urls': '',
            'no_of_external_links': 0,
            'author_name': '',
            'author_url': '',
            'claps': '',
            'reading_time': '',
            'keywords': ''
        }
        
        try:
            # Navigate to URL
            self.driver.get(url)
            
            # Wait for page to load - look for article content
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
            except:
                time.sleep(3)  # Fallback wait
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Extract Title
            try:
                title_elem = (
                    soup.find('h1') or 
                    soup.find('h1', class_='pw-post-title') or
                    soup.find(attrs={'data-testid': 'storyTitle'})
                )
                if title_elem:
                    data['title'] = title_elem.get_text(strip=True)
            except Exception as e:
                print(f"Title extraction error: {e}")
            
            # Extract Subtitle
            try:
                subtitle_elem = (
                    soup.find('h2', class_='pw-subtitle') or
                    soup.find('h2') or
                    soup.find('p', class_='pw-subtitle-paragraph')
                )
                if subtitle_elem and subtitle_elem != title_elem:
                    data['subtitle'] = subtitle_elem.get_text(strip=True)
            except Exception as e:
                print(f"Subtitle extraction error: {e}")
            
            # Extract Text (all paragraphs)
            try:
                article = soup.find('article')
                if article:
                    paragraphs = article.find_all('p')
                    text_content = ' '.join([p.get_text(strip=True) for p in paragraphs])
                    data['text'] = text_content
            except Exception as e:
                print(f"Text extraction error: {e}")
            
            # Extract Images
            try:
                article = soup.find('article')
                if article:
                    images = article.find_all('img')
                    image_urls = []
                    for img in images:
                        src = img.get('src', '')
                        if src and not src.startswith('data:'):
                            image_urls.append(src)
                    data['no_of_images'] = len(image_urls)
                    data['image_urls'] = ' | '.join(image_urls)
            except Exception as e:
                print(f"Image extraction error: {e}")
            
            # Extract External Links
            try:
                article = soup.find('article')
                if article:
                    links = article.find_all('a', href=True)
                    external_links = [
                        link['href'] for link in links 
                        if link['href'].startswith('http') and 'medium.com' not in link['href']
                    ]
                    data['no_of_external_links'] = len(external_links)
            except Exception as e:
                print(f"Links extraction error: {e}")
            
            # Extract Author Name and URL
            try:
                author_link = (
                    soup.find('a', rel='author') or
                    soup.find('a', attrs={'data-testid': 'authorName'}) or
                    soup.find('a', class_=re.compile(r'author', re.I))
                )
                if author_link:
                    data['author_name'] = author_link.get_text(strip=True)
                    data['author_url'] = author_link.get('href', '')
                    if data['author_url'] and not data['author_url'].startswith('http'):
                        data['author_url'] = 'https://medium.com' + data['author_url']
                
                # Fallback: check meta tags
                if not data['author_name']:
                    author_meta = soup.find('meta', property='author')
                    if author_meta:
                        data['author_name'] = author_meta.get('content', '')
            except Exception as e:
                print(f"Author extraction error: {e}")
            
            # Extract Claps
            try:
                # Look for clap button or count
                clap_elem = (
                    soup.find('button', attrs={'aria-label': re.compile(r'clap', re.I)}) or
                    soup.find('button', class_=re.compile(r'clap', re.I)) or
                    soup.find(text=re.compile(r'\d+\s*clap', re.I))
                )
                if clap_elem:
                    clap_text = clap_elem.get_text(strip=True) if hasattr(clap_elem, 'get_text') else str(clap_elem)
                    # Extract number from text
                    clap_match = re.search(r'(\d+[\d,]*)', clap_text)
                    if clap_match:
                        data['claps'] = clap_match.group(1).replace(',', '')
            except Exception as e:
                print(f"Claps extraction error: {e}")
            
            # Extract Reading Time
            try:
                # Look in meta tags first
                time_meta = soup.find('meta', property='twitter:data1')
                if time_meta:
                    data['reading_time'] = time_meta.get('content', '')
                
                # Fallback: search for reading time text
                if not data['reading_time']:
                    time_elem = soup.find(text=re.compile(r'\d+\s*min\s*read', re.I))
                    if time_elem:
                        time_match = re.search(r'(\d+)\s*min', str(time_elem), re.I)
                        if time_match:
                            data['reading_time'] = time_match.group(1) + ' min read'
            except Exception as e:
                print(f"Reading time extraction error: {e}")
            
            # Extract Keywords
            try:
                keywords = []
                
                # Method 1: Meta tags
                meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                if meta_keywords:
                    keywords.extend(meta_keywords.get('content', '').split(','))
                
                # Method 2: Links to tags/topics (most reliable)
                # Medium tags usually have href="/tag/..." or "/topic/..."
                tag_links = soup.find_all('a', href=re.compile(r'/(tag|topic)/'))
                for link in tag_links:
                    tag_text = link.get_text(strip=True)
                    if tag_text and len(tag_text) < 50:  # Avoid long link text
                        keywords.append(tag_text)
                
                # Clean and deduplicate
                # Remove duplicates while preserving order
                seen = set()
                unique_keywords = []
                for k in keywords:
                    k = k.strip()
                    if k and k.lower() not in seen:
                        seen.add(k.lower())
                        unique_keywords.append(k)
                
                data['keywords'] = ', '.join(unique_keywords[:10])  # Limit to 10 keywords
            except Exception as e:
                print(f"Keywords extraction error: {e}")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        return data
    
    def save_to_csv(self, data_list, mode='a'):
        """Save data to CSV"""
        df = pd.DataFrame(data_list)
        
        # Check if file exists to determine if we need headers
        file_exists = os.path.exists(self.output_csv)
        
        df.to_csv(self.output_csv, mode=mode, header=not file_exists, index=False, encoding='utf-8-sig')
        print(f"Saved {len(data_list)} records to {self.output_csv}")
    
    def scrape_all(self):
        """Main scraping function"""
        # Load URLs
        print(f"Loading URLs from {self.input_csv}...")
        urls_df = pd.read_csv(self.input_csv)
        all_urls = urls_df['url'].tolist()
        print(f"Total URLs to scrape: {len(all_urls)}")
        
        # Get already scraped URLs
        scraped_urls = self.get_scraped_urls()
        print(f"Already scraped: {len(scraped_urls)}")
        
        # Filter out scraped URLs
        urls_to_scrape = [url for url in all_urls if url not in scraped_urls]
        print(f"Remaining to scrape: {len(urls_to_scrape)}")
        
        if not urls_to_scrape:
            print("All URLs already scraped!")
            return
        
        # Setup driver
        print("Initializing browser...")
        self.setup_driver()
        
        # Scrape URLs
        batch_data = []
        
        try:
            for idx, url in enumerate(urls_to_scrape, 1):
                print(f"\n[{idx}/{len(urls_to_scrape)}] Scraping: {url}")
                
                # Extract data
                data = self.extract_data(url)
                batch_data.append(data)
                
                # Save checkpoint every N URLs
                if len(batch_data) >= self.checkpoint_interval:
                    self.save_to_csv(batch_data)
                    batch_data = []
                    print(f"Checkpoint saved. Progress: {idx}/{len(urls_to_scrape)}")
                
                # Random delay to avoid rate limiting
                delay = random.uniform(2, 5)
                print(f"Waiting {delay:.1f}s before next request...")
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\nScraping interrupted by user!")
        except Exception as e:
            print(f"\n\nUnexpected error: {e}")
        finally:
            # Save remaining data
            if batch_data:
                self.save_to_csv(batch_data)
                print(f"Final batch saved: {len(batch_data)} records")
            
            # Close browser
            if self.driver:
                self.driver.quit()
                print("Browser closed.")
        
        print(f"\n{'='*50}")
        print("Scraping completed!")
        print(f"Total scraped in this session: {idx}")
        print(f"Output saved to: {self.output_csv}")
        print(f"{'='*50}")

def main():
    """Entry point"""
    print("="*50)
    print("Medium Article Scraper")
    print("="*50)
    
    scraper = MediumScraper(
        input_csv='url_technology.csv',
        output_csv='scrapping_results.csv'
    )
    
    scraper.scrape_all()

if __name__ == "__main__":
    main()
