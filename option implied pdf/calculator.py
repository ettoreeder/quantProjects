import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.optimize import curve_fit
from scipy.special import wofz
import matplotlib.pyplot as plt

class Calculator:
    """
    Calculator class to compute the implied probability density function (PDF) from option prices.
    """
    def __init__(self, container):
        self.container = container

    def asymmetric_voigt(self, x, amplitude, center, sigma, gamma, asymmetry):
        z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2))
        voigt_profile = amplitude * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))
        asymmetry_factor = 1 + asymmetry * (x - center) / center
        return voigt_profile * asymmetry_factor

    def calculateImpliedPrice(self, strikePrices, prices):
        # Interpolate the strike prices and prices using PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
        strikePricesInterpolated= np.linspace(min(strikePrices), max(strikePrices), 1000)
        pricesSpline = PchipInterpolator(strikePrices, prices)
        pricesInterpolated = pricesSpline(strikePricesInterpolated)

        # Calculate the second derivative of the interpolated prices
        second_derivative = pricesSpline.derivative(nu=2)(strikePrices)

        # Fit an asymmetric Voigt profile to the second derivative
        initial_guess = [1.03831266e+00, 9.49497647e+04, 7.70953179e+03, 2.75680681e+03, 0.0]  # Initial guess for amplitude, center, sigma, gamma, asymmetry
        params, covariance = curve_fit(self.asymmetric_voigt, strikePrices, second_derivative, p0=initial_guess, bounds=(0, np.inf))
        amplitude, impliedPrice, sigma, gamma, asymmetry = params

        # Calculate standard deviation of the fit
        fitted_voigt = self.asymmetric_voigt(strikePrices, amplitude, impliedPrice, sigma, gamma, asymmetry)
        std = np.sqrt(np.sum(np.square(fitted_voigt-second_derivative)))/len(second_derivative)

        fig, axs = plt.subplots(2, 1, figsize=(10, 8))
        axs[0].plot(strikePrices, prices, 'x', label='imported data', color='blue')
        axs[0].plot(strikePricesInterpolated, pricesInterpolated, label='interpolated data', color='orange')
        axs[1].plot(strikePrices, second_derivative, 'x', label='second derivative', color='green')
        axs[1].plot(strikePrices, fitted_voigt, label='fitted Voigt profile', color='red')
        plt.show()

        return impliedPrice, std

    def calculateImpliedPrices(self):
        self.container.impliedPricesCall = {} # structure: {'times': [days_from_today1, days_from_today2, ...], 'impliedPrices': [impliedPrice1, impliedPrice2, ...], 'stds': [std1, std2, ...]}
        self.container.impliedPricesPut = {}  # structure: same as impliedPDFCall but for put options
        Ts, impliedPrices, stds = [], [], []
        for T, priceData in self.container.optionsDataCall.items():
            print(len(priceData[0]))
            strikePrices = priceData[0]
            prices = priceData[1]
            impliedPrice, std = self.calculateImpliedPrice(strikePrices, prices)
            Ts.append(T)
            impliedPrices.append(impliedPrice)
            stds.append(std)
        self.container.impliedPricesCall['times'] = Ts
        self.container.impliedPricesCall['impliedPrices'] = impliedPrices
        self.container.impliedPricesCall['stds'] = stds
        print(self.container.impliedPricesCall)


            