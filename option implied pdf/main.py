import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
import time
from calculator import Calculator
from plotter import Plotter
from importer import Importer
from container import Container
from tqdm import tqdm
import concurrent.futures
import ast


class Main():
    def __init__(self):
        self.container = Container()
        self.importer = Importer(self.container)
        self.calculator = Calculator(self.container)
        self.plotter = Plotter(self.container)

    def testing(self):
        self.importer.importOptionPriceData()
        self.calculator.calculateImpliedPrices()

if __name__ == "__main__":
    main = Main()
    main.testing()