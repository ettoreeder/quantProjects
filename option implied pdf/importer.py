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

    def insertOptionPriceData(self, targetDict, days_from_today, strikePrice, option):
        """
        Inserts option price data into the target dictionary.
        """
        if days_from_today not in targetDict:
            targetDict[days_from_today] = [[], []]
        targetDict[days_from_today][0].append(float(strikePrice))
        targetDict[days_from_today][1].append(float(option['mid_price']) * float(option['underlying_price']))

    def sortOptionPriceDict(self, dictToSort):
        """
        Sorts the dictionary by keys (days from today) and then sorts the inner lists by strike prices.
        """
        dictSorted = dict(sorted(dictToSort.items()))
        dictSortedRes = dictSorted.copy()
        for T, data in dictSorted.items():
            arr = np.array(data)
            # if len(arr[0]) < 20:
            #     del dictSortedRes[T]  # Remove entries with less than 20 strike prices
            # else:
            #     idx = np.argsort(arr[0])
            #     dictSortedRes[T] = arr[:, idx]
            idx = np.argsort(arr[0])
            dictSortedRes[T] = arr[:, idx]
        return dictSortedRes
    
    def importOptionPriceData(self):
        info_response = requests.get(self.container.fetchUrl)
        data = info_response.json()["result"]

        self.container.optionsDataCall = {} # structure: {days_from_today1: [[strikePrice1, strikePrice2, ...], [priceBTC1, priceBTC2, ...]], days_from_today2: [[strikePrice1, strikePrice2, ...], [priceBTC1, priceBTC2, ...]], ...}
        self.container.optionsDataPut = {} # structure: same as optionsDataCall but for put options
        for option in data:
            if option['mid_price'] is None:
                continue
            T, strikePrice, p_or_c = option['instrument_name'].split('-')[1:]
            # Convert T (format: 25JUL25) to a date object
            T_date = datetime.strptime(T, "%d%b%y").date()
            # Convert T_date to a number of days from today
            days_from_today = (T_date - datetime.today().date()).days
            if p_or_c == "C":
                self.insertOptionPriceData(self.container.optionsDataCall, days_from_today, strikePrice, option)
            elif p_or_c == "P":
                self.insertOptionPriceData(self.container.optionsDataPut, days_from_today, strikePrice, option)

        # Sort the dictionaries by keys (days from today) and then sort the inner lists by strike prices
        self.container.optionsDataCall = self.sortOptionPriceDict(self.container.optionsDataCall)
        self.container.optionsDataPut = self.sortOptionPriceDict(self.container.optionsDataPut)
