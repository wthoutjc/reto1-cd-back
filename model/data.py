import pandas as pd
from unicodedata import normalize
# Path: model\data.py
# Data extraction
from sodapy import Socrata

class Dataset:
    def __init__(self, url_connect, dataset_id):
        self.url_connect = url_connect
        self.dataset_id = dataset_id
        self.client = Socrata(self.url_connect, None)
        try:
            self.results = self.client.get(self.dataset_id, limit=100)
            self.df = pd.DataFrame(self.results)
            self.df['edad'] = self.df['edad'].apply(int)
        except:
            self.results = None
            self.df = None
    
    def __getitem__(self):
        return self.df.to_dict('records')

    def query(self, column, value):
        try:
            if type(value) == list:
                query = self.df.query(f"{column} > {value[0]} and {column} < {value[1]}")
                return query.to_dict('records')

            query = self.df.query(f"{column} == '{value}'")
            return query.to_dict('records')
        except Exception as e:
            print(e)
            return []

    def normalize_column(self, column: str):
        unicode = dict.fromkeys(map(ord, u'\u0301'))
        name = normalize('NFKC', normalize('NFKD', column).translate(unicode))
        name = name.replace(' ', '_')
        name = name.replace('_de_', '_')
        name = name.lower()

        return name

    def normalize_value(self, column: str, value: str):
        if column == 'edad':
            value = value.replace('[', '').replace(']', '').replace(' ', '')
            rango = [int(x) for x in value.split(',')]
            return rango

        if column == 'sexo':
            value = value[0:1]

        return value


    