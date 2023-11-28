import pathlib

import requests
from bs4 import BeautifulSoup
import re

def is_valid_link(url):
    try:
        response = requests.head(url, allow_redirects=True)
        # Consider any status code between 200 and 400 to be valid.
        return 200 <= response.status_code < 400
    except requests.RequestException:
        return False

def is_valid_image_url(url):
    try:
        response = requests.head(url, allow_redirects=True)  # Using HEAD to avoid downloading the whole content
        # Check if we got a successful response and if the content type indicates an image
        if response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower():
            return True
    except:
        pass

    return False

'''
for path in pathlib.Path('/Users/luoyu/PycharmProjects/chemwork/data/html/').iterdir():
    if path.is_file() and not path.stem.startswith('.'):

        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')

        # Find all http links
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', soup.get_text())
        urls = list(set(urls))
        # Extract src values (image links) from tags
        image_links = [img['src'] for img in img_tags if 'src' in img.attrs]
        image_links = list(set(image_links))
        print(path)
        for link in image_links:
            if 'gif' in link or 'jpg' in link or 'png' in link:
                if is_valid_image_url(link):
                    print(f"{link} is valid.")
                else:
                    for home_link in urls:
                        temp = home_link+link

                        if is_valid_image_url(temp):
                            print(f"{temp} is valid.")

        print("------------------")
        
'''


