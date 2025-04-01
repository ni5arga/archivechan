import re
import requests

def extract_emails_from_url(url):
    response = requests.get(url)
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
    return list(set(emails))
