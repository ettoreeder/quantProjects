import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
import time

class Container:
    def __init__(self):
        self.fetchUrl = 'https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option'
