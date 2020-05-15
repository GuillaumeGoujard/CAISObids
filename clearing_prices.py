import pandas as pd
import datetime
from pytz import timezone
import pytz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# gamma_prices["start_date"] >=shutoff_start
my_timezone=timezone('US/Pacific')


october = pd.read_csv("data/LMPs/20190915_20191013_PRC_LMP_DAM_20200511_15_28_17_v1.csv")
november = pd.read_csv("data/LMPs/20191012_20191106_PRC_LMP_DAM_20200511_15_31_06_v1.csv")
october_2018 = pd.read_csv("data/LMPs/20180916_20181014_PRC_LMP_DAM_20200511_16_07_08_v1.csv")
november_2018 = pd.read_csv("data/LMPs/20181013_20181107_PRC_LMP_DAM_20200511_16_08_16_v1.csv")

def treat_for_gamma(october):
    test = october[october["XML_DATA_ITEM"] == "LMP_ENE_PRC"]
    d = pd.to_datetime(test["INTERVALSTARTTIME_GMT"])
    test["start_date"] = d.apply(lambda s : s.astimezone(timezone('US/Pacific')))
    new_Df = pd.DataFrame()
    new_Df["start_date"] = test["start_date"]
    new_Df["gamma"] = test["MW"]
    new_Df = new_Df.sort_values(by='start_date')
    return new_Df

october =  treat_for_gamma(october)
november = treat_for_gamma(november)
gamma_prices = pd.concat([october, november]).drop_duplicates()
gamma_prices= gamma_prices.reset_index()

october_2018 = treat_for_gamma(october_2018)
november_2018 = treat_for_gamma(november_2018)
gamma_prices_2018 = pd.concat([october_2018, november_2018]).drop_duplicates()
gamma_prices_2018 = gamma_prices_2018.reset_index()

gamma_prices_2018["start_date"] = gamma_prices["start_date"]

def plot_prices_for_whole_period():
    shutoff_start = datetime.datetime(2019, 10, 9, tzinfo=timezone('US/Pacific'))
    shutoff_end = datetime.datetime(2019, 11, 1, tzinfo=timezone('US/Pacific'))

    pd.plotting.register_matplotlib_converters()
    fig, ax = plt.subplots(figsize=(15,8))

    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    # rotate and align the tick labels so they look better

    plt.plot(gamma_prices["start_date"], gamma_prices["gamma"], label="2019 prices")
    plt.plot(gamma_prices["start_date"], gamma_prices_2018["gamma"], label="2018 prices")
    ax.axvspan(shutoff_start, shutoff_end, alpha=0.1, color='red', label="outage period")
    fig.autofmt_xdate()
    plt.legend()
    plt.title("Marginal cost for CAISO from {} to {}".format(gamma_prices["start_date"].iloc[0].strftime("%Y-%m-%d"),
              gamma_prices["start_date"].iloc[-1].strftime("%Y-%m-%d")))
    plt.show()

    start = datetime.datetime(2019, 10, 5, tzinfo=timezone('US/Pacific'))
    shutoff_start = datetime.datetime(2019, 10, 9, tzinfo=timezone('US/Pacific'))
    shutoff_end = datetime.datetime(2019, 10, 16, tzinfo=timezone('US/Pacific'))

    example = gamma_prices[(gamma_prices["start_date"] >= start) & (gamma_prices["start_date"] <= shutoff_end)]
    example2018 = gamma_prices_2018[(gamma_prices["start_date"] >= start) & (gamma_prices["start_date"] <= shutoff_end)]
    pd.plotting.register_matplotlib_converters()
    fig, ax = plt.subplots(figsize=(15, 8))

    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    # rotate and align the tick labels so they look better

    plt.plot(example["start_date"], example["gamma"], label="2019 prices")
    plt.plot(example["start_date"], example2018["gamma"], label="2018 prices")
    ax.axvspan(shutoff_start, shutoff_end, alpha=0.1, color='red', label="outage period")
    fig.autofmt_xdate()
    plt.legend()
    plt.title("Marginal cost for CAISO from {} to {}".format(example["start_date"].iloc[0].strftime("%Y-%m-%d"),
                                                             example["start_date"].iloc[-1].strftime("%Y-%m-%d")))
    plt.show()


def compare_prices():
    ##second comparision
    shutoff_start = datetime.datetime(2019, 10, 9, tzinfo=timezone('US/Pacific'))
    shutoff_end = datetime.datetime(2019, 11, 1, tzinfo=timezone('US/Pacific'))

    before_outage_prices_2019 = gamma_prices[(gamma_prices["start_date"] <= shutoff_start)]
    outage_prices_2019 = gamma_prices[(gamma_prices["start_date"] >= shutoff_start) & (gamma_prices["start_date"]<=shutoff_end)]
    outage_prices_2018 = gamma_prices_2018[(gamma_prices_2018["start_date"] >= shutoff_start) & (gamma_prices_2018["start_date"]<=shutoff_end)]
    before_outage_prices_2019["2019 no outage prices"] = before_outage_prices_2019["gamma"]

    both_prices = pd.concat([outage_prices_2019["gamma"], outage_prices_2018["gamma"]], axis=1)
    both_prices.columns = ["2019 prices", "2018 prices"]
    fig, ax = plt.subplots(figsize=(10,8))
    both_prices.plot.kde(ax=ax, legend=True, title='Histogram: 2018 no shutoffs vs 2019 shutoffs')
    both_prices.plot.hist(density=True, ax=ax, bins=50, alpha=0.6)
    ax.set_ylabel('Probability')
    plt.xlim((-20, 200))
    ax.grid(axis='y')
    ax.set_facecolor('#d8dcd6')
    plt.show()

    ###
    fig, ax = plt.subplots(figsize=(10,8))
    both_prices["2019 prices"].plot.kde(ax=ax, legend=True, title='Histogram: A vs. B')
    before_outage_prices_2019["2019 no outage prices"].plot.kde(ax=ax, legend=True, title='Histogram: 2019 no shutoffs vs 2019 shutoffs')
    before_outage_prices_2019["2019 no outage prices"].plot.hist(density=True, legend=True, ax=ax, bins=50, alpha=0.6)
    both_prices["2019 prices"].plot.hist(density=True, ax=ax, legend=True, bins=50, alpha=0.6)
    ax.set_ylabel('Probability')
    ax.grid(axis='y')
    ax.set_facecolor('#d8dcd6')
    plt.xlim((-20, 200))
    plt.show()


if __name__ == '__main__':
    plot_prices_for_whole_period()
    compare_prices()


