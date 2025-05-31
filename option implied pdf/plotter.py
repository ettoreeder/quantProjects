import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.signal as sc
import time
from tqdm import tqdm
from scipy.interpolate import interp1d
import matplotlib.cm as cm
import matplotlib.colors as mcolors

class Plotter():
    def __init__(self, container):
        self.container = container