"""
Test script to verify the Medium scraper on a small sample
"""
import sys
from medium_scraper import MediumScraper

def test_scraper():
    """Test with 3 sample URLs"""
    print("="*60)
    print("MEDIUM SCRAPER - TEST MODE")
    print("="*60)
    print("\nTesting with 3 sample URLs...")
    
    # Use test CSV
    scraper = MediumScraper(
        input_csv='test_urls.csv',
        output_csv='test_results.csv'
    )
    
    # Run scraper
    scraper.scrape_all()
    
    print("\n" + "="*60)
    print("Test completed! Check 'test_results.csv' for results")
    print("="*60)

if __name__ == "__main__":
    test_scraper()
