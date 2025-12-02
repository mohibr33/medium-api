# Medium Article Scraper

A Python scraper to extract data from Medium articles, bypassing anti-bot protection.

## Features

- **Extracts all required data**:
  - Title
  - Subtitle
  - Full text content
  - Number of images & image URLs
  - Number of external links
  - Author name & URL
  - Claps count
  - Reading time
  - Keywords

- **Robust & Reliable**:
  - Uses Selenium with undetected-chromedriver to bypass Cloudflare
  - Auto-saves progress every 100 URLs
  - Resume capability (skips already scraped URLs)
  - Error handling for each field
  - Random delays (2-5s) to avoid rate limiting

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Chrome browser required** (will be used by Selenium)

## Usage

### Run the scraper
```bash
python medium_scraper.py
```

The scraper will:
1. Load URLs from `url_technology.csv`
2. Check for already scraped URLs in `scrapping_results.csv`
3. Start scraping remaining URLs
4. Save progress every 100 URLs
5. Output final results to `scrapping_results.csv`

### Resume after interruption

Simply run the script again:
```bash
python medium_scraper.py
```

It will automatically skip URLs that are already in `scrapping_results.csv`

## Files

- `medium_scraper.py` - Main scraper script
- `url_technology.csv` - Input file with 58,100 Medium URLs
- `scrapping_results.csv` - Output file (created automatically)
- `requirements.txt` - Python dependencies

## Output Format

CSV file with columns:
- `url` - Article URL
- `title` - Article title
- `subtitle` - Article subtitle
- `text` - Full article text
- `no_of_images` - Count of images
- `image_urls` - Pipe-separated image URLs
- `no_of_external_links` - Count of external links
- `author_name` - Author name
- `author_url` - Author profile URL
- `claps` - Number of claps
- `reading_time` - Estimated reading time
- `keywords` - Comma-separated keywords

## Estimated Time

- ~58,000 URLs with 2-5 second delays
- **Estimated total time**: 32-72 hours

## Notes

- The browser window will open (can be hidden by uncommenting headless mode in code)
- Progress is printed to console
- Internet connection required
- May encounter Cloudflare checks occasionally (script will handle)

## Troubleshooting

**Chrome driver issues**:
- Undetected-chromedriver will auto-download the correct version
- If issues persist, update Chrome browser to latest version

**Rate limiting**:
- Increase delay range in code if getting blocked
- Script already includes 2-5s random delays

**Memory issues**:
- Script saves every 100 URLs to avoid memory buildup
- Can adjust `checkpoint_interval` in code if needed
