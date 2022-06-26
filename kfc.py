import json
from requests_html import HTMLSession


class Parser:

    def __init__(self):
        self.session = HTMLSession()
        self.url = 'https://www.kfc.ru/api/restaurants/list/?restautantId'
        self.restaurants = []
        self.json = 'restaurants.json'

    def processing_data(self):
        result = self.session.get(url=self.url)
        all_data = result.json()
        for data in all_data['restaurants']:
            working_hours = []
            workdays_hours = data['hoursOfOperation']['workdays']
            weekends_hours = data['hoursOfOperation']['weekends']
            working_hours.append(f"Пн-Пт {workdays_hours.get ('startStr')} - {workdays_hours.get ('endStr')}")
            working_hours.append(f"Сб-Вс {weekends_hours.get ('startStr')} - {weekends_hours.get ('endStr')}")
            if not weekends_hours['isDayOff']:
                working_hours.append(f"Сб-Вс {weekends_hours.get ('startStr')} - {weekends_hours.get ('endStr')}")
            self.restaurants.append(
                {
                    'address': data['address'],
                    'latlon': [float(data['latitude']), float(data['longitude'])],
                    'name': data['name'],
                    'phones': data['phone'].split(';'),
                    'working_hours': working_hours,

                }
            )

    def write_file(self):
        self.processing_data()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.restaurants, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()



