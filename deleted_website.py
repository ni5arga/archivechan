import requests
from bs4 import BeautifulSoup
import urllib.parse

def resurrect_deleted_site(url, output_dir):
    cache_urls = [
        f"http://web.archive.org/web/{url}",
        f"https://archive.today/{urllib.parse.quote(url)}",
        f"https://google.com/search?q=cache:{url}"
    ]
    for cache in cache_urls:
        try:
            r = requests.get(cache, timeout=10)
            if r.status_code == 200:
                with open(f"{output_dir}/resurrected.html", "wb") as f:
                    f.write(r.content)
                return True
        except:
            continue
    return False
