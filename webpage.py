# archivechan
# script to archive webapages

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime

def archive_webpage(url, output_dir='archived_pages'):
    """Archive a single webpage with all its resources"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path[1:] if parsed_url.path else 'index'
        
        domain_dir = os.path.join(output_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        clean_path = ''.join(c if c.isalnum() else '_' for c in path)
        if not clean_path:
            clean_path = 'index'
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{clean_path}.html"
        filepath = os.path.join(domain_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Successfully archived: {url} -> {filepath}")
        return filepath
    
    except Exception as e:
        print(f"Failed to archive {url}: {str(e)}")
        return None

if __name__ == "__main__":
    url = input("Enter URL to archive: ")
    archive_webpage(url)
