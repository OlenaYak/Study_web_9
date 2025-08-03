import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def parse_author(author_url):
    soup = get_soup(BASE_URL + author_url)
    fullname = soup.find('h3', class_='author-title').text.strip() # type: ignore
    born_date = soup.find('span', class_='author-born-date').text.strip() # type: ignore
    born_location = soup.find('span', class_='author-born-location').text.strip() # type: ignore
    description = soup.find('div', class_='author-description').text.strip() # type: ignore

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def scrape_site():
    page_url = '/page/1/'
    quotes = []
    authors = {}
    
    while page_url:
        soup = get_soup(BASE_URL + page_url) # type: ignore
        quote_blocks = soup.select('div.quote')
        
        for quote_block in quote_blocks:
            text = quote_block.find('span', class_='text').text.strip() # type: ignore
            author = quote_block.find('small', class_='author').text.strip() # type: ignore
            tags = [tag.text for tag in quote_block.select('div.tags a.tag')]
            
            quotes.append({
                "tags": tags,
                "author": author,
                "quote": text
            })
            
            author_relative_url = quote_block.find('a')['href'] # type: ignore
            if author not in authors:
                authors[author] = parse_author(author_relative_url)
        
        next_btn = soup.select_one('li.next a')
        page_url = next_btn['href'] if next_btn else None

    return quotes, list(authors.values())

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    quotes, authors = scrape_site()
    save_json('qoutes.json', quotes)
    save_json('authors.json', authors)
