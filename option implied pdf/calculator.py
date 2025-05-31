import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import time
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

class Calculator:
    def __init__(self, container):
        self.container = container