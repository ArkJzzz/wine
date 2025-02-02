import os
import datetime
import collections

import pandas
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    winery_foundation_year = 1920
    today = datetime.date.today()
    winery_age = today.year - winery_foundation_year

    load_dotenv()
    excel_data_df = pandas.read_excel(
                io=os.getenv('WINES_FILEPATH'),
                sheet_name='Лист1',
                na_values='nan',
                keep_default_na=False,
            )
    bottles = excel_data_df.to_dict('records')
    assortment = collections.defaultdict(list)
    for bottle in bottles:
        assortment[bottle['Категория']].append(bottle)
    assortment = collections.OrderedDict(sorted(assortment.items()))

    rendered_page = template.render(
        winery_age=winery_age,
        assortment=assortment,
    )
    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()