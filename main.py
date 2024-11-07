import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://quotes.toscrape.com/'


def scrape_quotes(base_url):
    quotes_list = []
    next_page = base_url

    while next_page:
        response = requests.get(next_page)
        if response.status_code != 200:
            print(f'Ошибка: {response.status_code}')
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.select('.quote')

        for quote in quotes:
            text = quote.select_one('.text').get_text(strip=True)
            author = quote.select_one('.author').get_text(strip=True)
            tags = [tag.get_text(strip=True)
                    for tag in quote.select('.tags .tag')]

            quotes_list.append({
                'text': text,
                'author': author,
                'tags': tags
            })

        next_button = soup.select_one('.pager .next a')
        if next_button:
            next_page = base_url + next_button['href']
        else:
            next_page = None

    return quotes_list


if __name__ == '__main__':
    data = scrape_quotes(BASE_URL)
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print('Данные успешно сохранены в файл quotes.json')
