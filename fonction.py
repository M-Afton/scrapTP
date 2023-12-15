import json
from bs4 import BeautifulSoup
import requests
import sqlalchemy as db
import csv

class DataBase():
    def __init__(self, name_database='database'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()

    def create_table(self, name_table, **kwargs):
        columns = [db.Column(k, v, primary_key=True) if 'id_' in k else db.Column(k, v) for k, v in kwargs.items()]
        table = db.Table(name_table, self.metadata, *columns, extend_existing=True)
        self.metadata.create_all(self.engine)
        print(f"Table '{name_table}' created successfully")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        return table.columns.keys() if return_keys else table

    def add_row(self, name_table, **kwargs):
        table = self.read_table(name_table)
        stmt = db.insert(table).values(kwargs)
        self.connection.execute(stmt)
        print(f'Row added to {name_table}')

    def delete_row_by_id(self, name_table, id_):
        table = self.read_table(name_table)
        stmt = db.delete(table).where(table.c.id_ == id_)
        self.connection.execute(stmt)
        print(f'Row with id {id_} deleted')

    def select_table(self, name_table):
        table = self.read_table(name_table)
        stmt = db.select([table])
        return self.connection.execute(stmt).fetchall()

def scraping_and_store(pages=1):
    base_url = 'https://noveldeglace.com/nouvelles/page/'
    # Initialize the database
    database = DataBase(name_database='MaBaseDeDonnees')

    # Define the table structure (you can adjust this based on your needs)
    table_structure = {
        'id': db.Integer,
        'title': db.String,
        'date': db.String,
        'link': db.String,
        'image': db.String,
        'categorie': db.String
    }

    # Create the table
    database.create_table('Tableau1', **table_structure)

    # Initialize the article list
    article_list = []

    for page_num in range(1, pages + 1):
        url = f'{base_url}{page_num}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article')

        for article in articles:
            article_data = {}

            id = article.get('id')
            article_data['title'] = article.find('h2').text.replace('\xa0', ' ')

            try:
                image = article.find('img')['src']
                article_data['image'] = image
            except TypeError:
                article_data['image'] = None

            try:
                link = article.find('a', rel='tag')['href']
                article_data['link'] = link
            except TypeError:
                article_data['link'] = None

            try:
                date = article.find('a', rel='bookmark').text
                article_data['date'] = date
            except AttributeError:
                article_data['date'] = None

            try:
                msg = article.select_one('div.entry-summary p').text
                article_data['categorie'] = msg
            except AttributeError:
                article_data['categorie'] = None

            article_list.append(article_data)

    # Store data in CSV
    with open('bdm.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'date', 'link', 'image', 'categorie']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write a separation line
        writer.writerow({'title': '-------------------------------------------'})

        # Write the new data
        for row in article_list:
            writer.writerow(row)

    # Store data in the database
    for article_data in article_list:
        database.add_row('Tableau1', **article_data)

    return article_list
if __name__ == "__main__":
    scraping_and_store()
