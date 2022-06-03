import pandas as pd

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
        except:
            self.results = None
    
    def __getitem__(self):
        return pd.DataFrame(self.results).to_dict('records')