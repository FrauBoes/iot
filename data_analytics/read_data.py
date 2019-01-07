# import pandas as pd
from pandas import Series
from matplotlib import pyplot

series = Series.from_csv("1917-2017.csv", header=5)
# print(series.head())

# Center-rolling average transform
rolling = series.rolling(window=12, center=True)
rolling_mean = rolling.mean()
standard_deviation = rolling.std()

print(standard_deviation.head(12))

# series.plot()
rolling_mean.plot(color='red')
standard_deviation.plot(color='green')

pyplot.show()

# Average
# average = series.mean('value')
# print(average)
