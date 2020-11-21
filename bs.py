import os
import requests
from bs4 import BeautifulSoup

def save_soup_as_html(soup_obj, filepath: str):
    html_string = str(soup_obj)

    dir_path, _ = os.path.split(filepath)
    os.makedirs(dir_path, exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(html_string)

def try_load_html_as_soup(filepath: str, url: str):
    try:
        with open(filepath, 'r') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
    except FileNotFoundError as e:
        print(e)
        print('Getting html from backup URL: {}'.format(url))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        print('Saving html to {}...'.format(filepath))
        save_soup_as_html(soup, filepath)
    return soup
