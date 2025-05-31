import numpy as np
import requests

class Importer:
    def __init__(self, container):
        self.container = container
    
    def importOptionPriceData(self):
        info_response = requests.get(self.container.fetchUrl)
        data = info_response.json()["result"]

        self.container.optionsDataCall = {}
        self.container.optionsDataPut = {}
        for option in data:
            T, strikePrice, p_or_c = option['instrument_name'].split('-')[1:]
            