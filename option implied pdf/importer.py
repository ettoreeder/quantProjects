import numpy as np
import requests
from datetime import datetime

class Importer:
    """
    Importer class to fetch option price data from the Deribit API and store it in the container.
    This class is responsible for making the API call and processing the response to extract relevant option data.
    """
    def __init__(self, container):
        self.container = container
    
    def importOptionPriceData(self):
        info_response = requests.get(self.container.fetchUrl)
        data = info_response.json()["result"]

        self.container.optionsDataCall = {} # structure: {T1: [(strikePrice1, priceBTC1), (strikePrice2, priceBTC2), ...], T2: [(strikePrice1, priceBTC1), ...], ...}
        self.container.optionsDataPut = {} # structure: same as optionsDataCall but for put options
        for option in data:
            T, strikePrice, p_or_c = option['instrument_name'].split('-')[1:]
            # Convert T (format: 25JUL25) to a date object
            T_date = datetime.strptime(T, "%d%b%y").date()
            # Convert T_date to a number of days from today
            days_from_today = (T_date - datetime.today().date()).days
            if option['mid_price'] is None:
                continue
            if p_or_c == "P":
                if days_from_today not in self.container.optionsDataPut:
                    self.container.optionsDataPut[days_from_today] = []
                self.container.optionsDataPut[days_from_today].append((float(strikePrice), float(option['mid_price']) * float(option['underlying_price'])))
            elif p_or_c == "C":
                if days_from_today not in self.container.optionsDataCall:
                    self.container.optionsDataCall[days_from_today] = []
                self.container.optionsDataCall[days_from_today].append((float(strikePrice), float(option['mid_price']) * float(option['underlying_price'])))

        # Sort the options data by expiration date
        self.container.optionsDataCall = dict(sorted(self.container.optionsDataCall.items()))
        self.container.optionsDataPut = dict(sorted(self.container.optionsDataPut.items()))