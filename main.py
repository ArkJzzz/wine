import datetime
import collections
from pprint import pprint

import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_foundation = datetime.date(year=1920, month=1, day=1)
today = datetime.date.today()
winery_age = today.year - winery_foundation.year

excel_data_df = pandas.read_excel(
            io='wine3.xlsx',
            sheet_name='Лист1',
            na_values='nan',
            keep_default_na=False,
        )
bottles = excel_data_df.to_dict('records')
categories = collections.defaultdict(list)

for bottle in bottles:
    categories[bottle['Категория']].append(
            {
                'title': bottle['Название'],
                'variety': bottle['Сорт'],
                'price': bottle['Цена'],
                'image': bottle['Картинка'],
                'promotion': bottle['Акция']
            }
        )

rendered_page = template.render(
    winery_age=winery_age,
    categories=categories,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
