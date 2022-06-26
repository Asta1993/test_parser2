import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession


class Parser:

    def __init__(self):
        self.session = HTMLSession()
        self.url = 'https://monomax.by/map'
        self.json = 'all_shops.json'
        self.result = []

    def get_html(self):
        result_html = self.session.get(url=self.url)
        soup = BeautifulSoup(result_html.text, 'html.parser')
        items = soup.find_all ('div', class_='all-shops')
        for item in items:
            shop = item.find_all('div', {'class': 'shop'})
            [self.get_content(shop) for shop in shop]

    def get_content(self, shop):
        self.result.append({
            'address': f"{shop['name']}",
            'latlon': [float(shop['latitude']), float(shop['longitude'])],
            'name': ['Мономах'],
            'phones': shop['phone']
        })

    def write_file(self):
        self.get_html()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.result, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()