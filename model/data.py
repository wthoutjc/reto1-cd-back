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
            self.results = self.client.get(self.dataset_id, limit=1000)
            self.df = pd.DataFrame(self.results)
            self.df['id_de_caso'] = self.df['id_de_caso'].astype(str).astype(int)
            self.df['departamento'] = self.df['departamento'].astype(str).astype(int)
            self.df['ciudad_municipio'] = self.df['ciudad_municipio'].astype(str).astype(int)
            self.df['edad'] = self.df['edad'].astype(str).astype(int)
            self.df['fecha_reporte_web'] = pd.to_datetime(self.df['fecha_reporte_web'])
            self.df['fecha_de_notificaci_n'] = pd.to_datetime(self.df['fecha_de_notificaci_n'])
            self.df['fecha_inicio_sintomas'] = pd.to_datetime(self.df['fecha_inicio_sintomas'])
            self.df['fecha_diagnostico'] = pd.to_datetime(self.df['fecha_diagnostico'])
            self.df['fecha_recuperado'] = pd.to_datetime(self.df['fecha_recuperado'])
            self.df['fecha_muerte'] = pd.to_datetime(self.df['fecha_muerte'])
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


    