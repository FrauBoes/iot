from pandas import Series, stats
from matplotlib import pyplot

ewma = stats.moments.ewma

series = Series.from_csv("1917-2017.csv", header=5)
# print(series.head())

# Center-rolling average transform
rolling = series.rolling(window=12, center=True)
rolling_mean = rolling.mean()

fw_exp_wm_avg = ewma(series, span=12, min_periods=12)
bw_exp_wm_avg = ewma(series [::-1], span=12, min_periods=12)

# series.plot()
fw_exp_wm_avg.plot(color='green')
bw_exp_wm_avg.plot(color='yellow')

pyplot.show()

# Average
# average = series.mean('value')
# print(average)
