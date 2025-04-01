import os
import requests
import re
from bs4 import BeautifulSoup

def download_instagram_images(username, count=20, output_dir='instagram_downloads'):
    os.makedirs(output_dir, exist_ok=True)
    url = f"https://www.instagram.com/{username}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', text=re.compile('window\._sharedData'))
    json_data = script.text.split(' = ')[1].rstrip(';')
    media = json.loads(json_data)['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    downloaded = 0
    for item in media[:count]:
        try:
            img_url = item['node']['display_url']
            img_data = requests.get(img_url).content
            filename = f"{username}_{item['node']['shortcode']}.jpg"
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(img_data)
            downloaded += 1
        except:
            continue
    return downloaded
