import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def download_images(url, output_dir='downloaded_images', file_types=('jpg', 'jpeg', 'png', 'gif')):
    """Download all images from a webpage"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        img_tags = soup.find_all('img')
        image_urls = [img.get('src') for img in img_tags if img.get('src')]
        
        style_tags = soup.find_all(style=re.compile(r'background-image:\s*url\(.*\)'))
        for tag in style_tags:
            match = re.search(r'background-image:\s*url\((.*?)\)', tag['style'])
            if match:
                image_urls.append(match.group(1))
        
        downloaded = 0
        for img_url in image_urls:
            try:
                # handle relative URLs
                img_url = urljoin(url, img_url)
                
                if not img_url.lower().endswith(file_types):
                    continue
                
                filename = os.path.basename(img_url.split('?')[0])
                if not filename:
                    continue
                
                img_data = requests.get(img_url, headers=headers).content
                filepath = os.path.join(output_dir, filename)
                
                counter = 1
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(filename)
                    filepath = os.path.join(output_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                
                downloaded += 1
                print(f"Downloaded: {filename}")
                
            except Exception as e:
                print(f"Failed to download {img_url}: {str(e)}")
        
        print(f"\nDownloaded {downloaded} images from {url}")
        
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    url = input("Enter URL to download images from: ")
    download_images(url)
