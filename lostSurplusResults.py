# import pandas as pd
# import datetime
# from pytz import timezone
# import pytz
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# # gamma_prices["start_date"] >=shutoff_start
# my_timezone=timezone('US/Pacific')
#
#
# october = pd.read_csv("data/LMPs/20190915_20191013_PRC_LMP_DAM_20200511_15_28_17_v1.csv")
# november = pd.read_csv("data/LMPs/20191012_20191106_PRC_LMP_DAM_20200511_15_31_06_v1.csv")
# october_2018 = pd.read_csv("data/LMPs/20180916_20181014_PRC_LMP_DAM_20200511_16_07_08_v1.csv")
# november_2018 = pd.read_csv("data/LMPs/20181013_20181107_PRC_LMP_DAM_20200511_16_08_16_v1.csv")
#
# def treat_for_gamma(october):
#     test = october[october["XML_DATA_ITEM"] == "LMP_ENE_PRC"]
#     d = pd.to_datetime(test["INTERVALSTARTTIME_GMT"])
#     test["start_date"] = d.apply(lambda s : s.astimezone(timezone('US/Pacific')))
#     new_Df = pd.DataFrame()
#     new_Df["start_date"] = test["start_date"]
#     new_Df["gamma"] = test["MW"]
#     new_Df = new_Df.sort_values(by='start_date')
#     return new_Df
#
# october =  treat_for_gamma(october)
# november = treat_for_gamma(november)
# gamma_prices = pd.concat([october, november]).drop_duplicates()
# gamma_prices= gamma_prices.reset_index()
#
# october_2018 = treat_for_gamma(october_2018)
# november_2018 = treat_for_gamma(november_2018)
# gamma_prices_2018 = pd.concat([october_2018, november_2018]).drop_duplicates()
# gamma_prices_2018 = gamma_prices_2018.reset_index()
#
# gamma_prices_2018["start_date"] = gamma_prices["start_date"]
#
# """
# TEST 2
# """
# return_df = pd.read_csv("results2.csv")
# return_df["start_date"] = return_df["Unnamed: 0"]
# return_df["start_date"] = pd.to_datetime(return_df["start_date"]).apply(lambda d : timezone('US/Pacific').localize(d))
# return_df.drop_duplicates()
#
# shutoff_start = return_df["start_date"].iloc[0]
# shutoff_end = return_df["start_date"].iloc[-1]
#
# pd.plotting.register_matplotlib_converters()
#
# example = gamma_prices[(gamma_prices["start_date"] >= shutoff_start) & (gamma_prices["start_date"] <= shutoff_end)]
# example2018 = gamma_prices_2018[(gamma_prices["start_date"] >= shutoff_start) & (gamma_prices["start_date"] <= shutoff_end)]
# fig, ax = plt.subplots(figsize=(15,8))
#
# formatter = mdates.DateFormatter("%Y-%m-%d")
# ax.xaxis.set_major_formatter(formatter)
#
# locator = mdates.DayLocator()
# ax.xaxis.set_major_locator(locator)
# # rotate and align the tick labels so they look better
#
# plt.plot(example["start_date"], example["gamma"], label="2019 prices")
# plt.plot(example["start_date"], example2018["gamma"], label="2018 prices")
# plt.plot(example["start_date"], return_df["actual cleared price"], label="2019 equilibrium prices")
# plt.plot(example["start_date"], return_df["expected cleared price"], label="2019 expected equilibrium prices")
# # ax.axvspan(shutoff_start, shutoff_end, alpha=0.1, color='red', label="outage period")
# fig.autofmt_xdate()
# plt.legend()
# plt.title("Marginal cost for CAISO from {} to {}".format(gamma_prices["start_date"].iloc[0].strftime("%Y-%m-%d"),
#           gamma_prices["start_date"].iloc[-1].strftime("%Y-%m-%d")))
# plt.show()
#
#
# """
# test
# """
# test = return_df["actual cleared price"].values - example["gamma"].values
# test_df = pd.DataFrame(data = test)
# fig, ax = plt.subplots(figsize=(10,8))
# test_df.plot.kde(ax=ax, legend=True, title='Histogram: Errors in 2019 clearing prices')
# # before_outage_prices_2019["2019 no outage prices"].plot.kde(ax=ax, legend=True, title='Histogram: 2019 no shutoffs vs 2019 shutoffs')
# test_df.plot.hist(density=True, legend=True, ax=ax, bins=50, alpha=0.6)
# # both_prices["2019 prices"].plot.hist(density=True, ax=ax, legend=True, bins=50, alpha=0.6)
# ax.set_ylabel('Probability')
# ax.grid(axis='y')
# ax.set_facecolor('#d8dcd6')
# plt.xlim((-25, 25))
# plt.show()
#
# import numpy as np
# np.mean(test_df)
# np.std(test_df)
# errors = abs(test_df)
# errors.describe()
#
# pd.plotting.register_matplotlib_converters()
# fig, ax = plt.subplots(figsize=(15, 8))
# formatter = mdates.DateFormatter("%Y-%m-%d")
# ax.xaxis.set_major_formatter(formatter)
#
# locator = mdates.DayLocator()
# ax.xaxis.set_major_locator(locator)
# # rotate and align the tick labels so they look better
# plt.plot(return_df["start_date"], return_df["Lost Surplus"])
# fig.autofmt_xdate()
# plt.axhline(y=0, color="black")
# plt.xlabel("Date")
# plt.ylabel("Lost Surplus (USD)")
# plt.legend()
# plt.show()
#
# result = return_df.describe()
# print(result.round(1).to_latex())
#
# sum(return_df["Lost Surplus"])
#
