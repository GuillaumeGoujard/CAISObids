import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import intersect

df = pd.read_csv("data/public_bids/20191024_20191024_PUB_BID_DAM_v2.csv")
df_2018 = pd.read_csv("data/public_bids/20181025_20181025_PUB_BID_DAM_v2.csv")
test = df.describe()

def treat_df(df):
    df["start_date"] = pd.to_datetime(df["TIMEINTERVALSTART"])
    df["end_date"] = pd.to_datetime(df["TIMEINTERVALEND"])
    bids_time_treated = pd.to_datetime(df["SCH_BID_TIMEINTERVALSTART"]).dropna()
    df.loc[bids_time_treated.index, "start_date"] = bids_time_treated
    bids_time_treated = pd.to_datetime(df["SCH_BID_TIMEINTERVALSTOP"]).dropna()
    df.loc[bids_time_treated.index, "end_date"] = bids_time_treated
    df = df[df["MARKETPRODUCTTYPE"]=="EN"]
    return df

df = treat_df(df)
df_2018 = treat_df(df_2018)

hour = 18
date = df["start_date"].iloc[0]
eight_hour_datetime = datetime.datetime(date.year, date.month, date.day, hour)

# date = df["start_date"].iloc[0]
# eight_hour_datetime = datetime.datetime(date.year, date.month, date.day, 8)
# date_2018 = df_2018["start_date"].iloc[0]
# eight_hour_datetime_2018 = datetime.datetime(date_2018.year, date_2018.month, date_2018.day, 8)
# bids_for_eight = df[(df["start_date"]<=eight_hour_datetime) & (df["end_date"]>=eight_hour_datetime+datetime.timedelta(hours=1))]
# bids_for_eight_2018 = df_2018[(df_2018["start_date"]<=eight_hour_datetime_2018) & (df_2018["end_date"]>=eight_hour_datetime_2018+datetime.timedelta(hours=1))]

"""
load
"""
# demand = pd.read_csv("data/20191010_20191011_ENE_SLRS_DAM_20200511_12_10_51_v1.csv")
# load = demand[demand["SCHEDULE"]=="Load"].groupby("OPR_HR").sum()["MW"]
# load_CAISO = demand[(demand["SCHEDULE"]=="Load") & (demand["TAC_ZONE_NAME"]=="Caiso_Totals")]
# set(demand["TAC_ZONE_NAME"])


"""
First try plot the supply curve of one actor

One generator 
"""
# bids_for_eight.groupby("RESOURCEBID_SEQ").count()
#477 bidding resource
#ex for RESOURCEBID_SEQ == 100454
# t = test[test["STARTTIME"]>5]
# for gen_id in t.index[14:]:
#     input("enter")
# gen_id = 160605
# print(gen_id)
# bidding_curve = bids_for_eight[bids_for_eight["RESOURCEBID_SEQ"]==gen_id]
# bidding_curve = bidding_curve.sort_values(by='SCH_BID_Y1AXISDATA')
# bidding_curve['cumsum_MW'] = bidding_curve['SCH_BID_XAXISDATA'] #.cumsum()
# l0 = list(bidding_curve['cumsum_MW'])
# l1 = list(bidding_curve['SCH_BID_Y1AXISDATA'])
# plt.figure(figsize=(10,8))
# plt.step([0]+ l0, [l1[0]] +l1)
# plt.axhline(y=39.7, color="red", label="clearing price : \$39.7")
# plt.axvline(x=160, color="black", label="clearing volume for generator : 160MWh")
# plt.grid(True)
# plt.xlabel("Cumulated bids (MWh)")
# plt.ylabel("Bid price (USD/MWh)")
# plt.title("Bids for generator {}, on {}".format(gen_id, str(eight_hour_datetime)))
# plt.legend()
# y1 = [l1[0], l1[0], l1[1], l1[1]]
# y2 = [39.7, 39.7, 39.7, 39.7]
# plt.fill_between([0,l0[0]]+ l0[:2], y1, y2, where=(y1 < y2), alpha=0.5, color="yellow")
# plt.show()
# 39.5*160 - 35.58*83 -38.3*(160-83)
"""
Set of interties
"""
# set(bids_for_eight["RESOURCE_TYPE"])
# bids_for_eight[bids_for_eight["RESOURCE_TYPE"] == "INTERTIE"].groupby("RESOURCEBID_SEQ").count()
# #193 intertie
# bidding_curve = bids_for_eight[bids_for_eight["RESOURCEBID_SEQ"]==101767]
# # bidding_curve = bidding_curve.sort_values(by='SCH_BID_Y1AXISDATA')
# bidding_curve['cumsum_MW'] = bidding_curve['SCH_BID_XAXISDATA'] #.cumsum()
# l0 = list(bidding_curve['cumsum_MW'])
# l1 = list(bidding_curve['SCH_BID_Y1AXISDATA'])
# plt.figure(figsize=(10,8))
# plt.step([0]+ l0, [l1[0]] +l1)
# plt.grid(True)
# plt.xlabel("Cumulated bids (MWh)")
# plt.ylabel("Bid price (USD/MWh)")
# plt.title("Demand bids for intertie 101767, on {}".format(str(eight_hour_datetime)))
# plt.show()

"""
Set of loads
"""
# set(bids_for_eight["RESOURCE_TYPE"])

# t = bids_for_eight[bids_for_eight["RESOURCE_TYPE"] == "LOAD"].groupby("RESOURCEBID_SEQ").count()
# #193 intertie
# bidding_curve = bids_for_eight[bids_for_eight["RESOURCEBID_SEQ"]==199635].iloc[1:]
# # bidding_curve = bidding_curve.sort_values(by='SCH_BID_Y1AXISDATA')
# bidding_curve['cumsum_MW'] = bidding_curve['SCH_BID_XAXISDATA'] #.cumsum()
# l0 = list(bidding_curve['cumsum_MW'])
# l1 = list(bidding_curve['SCH_BID_Y1AXISDATA'])
# plt.figure(figsize=(10,8))
# plt.step([0]+ l0, [l1[0]] +l1)
# plt.grid(True)
#
# plt.xlabel("Cumulated bids (MWh)")
# plt.ylabel("Bid price (USD/MWh)")
# plt.title("Demand bids for load 199635, on {}".format(str(eight_hour_datetime)))
# plt.show()


# bids_for_eight = df[(df["start_date"]>=eight_hour_datetime) & (df["end_date"]<=eight_hour_datetime+datetime.timedelta(hours=1))]
"""
Reconstruct supply 
"""
def get_generator_bids(bids_for_eight):
    generator_bids = bids_for_eight[bids_for_eight["RESOURCE_TYPE"].isin(["GENERATOR", "INTERTIE"])]
    # generator_bids.groupby("RESOURCEBID_SEQ").count()
    # test = generator_bids[~generator_bids["SELFSCHEDMW"].isna()]
    self_schedule_for_eight = sum(generator_bids["SELFSCHEDMW"].dropna())
    generator_bids = generator_bids[(generator_bids["SELFSCHEDMW"].isna())]

    generator_bids["unitMW"] = 0
    for gen_id in set(generator_bids["RESOURCEBID_SEQ"][generator_bids["RESOURCE_TYPE"]=="GENERATOR"]):
        bidding_curve = generator_bids[generator_bids["RESOURCEBID_SEQ"] == gen_id]
        test = pd.concat([bidding_curve["SCH_BID_XAXISDATA"], bidding_curve["SCH_BID_XAXISDATA"].shift(1, fill_value=0)], axis=1)
        test2 = test.iloc[:,0] - test.iloc[:,1]
        test2 = test2.apply(lambda x : max(0,x))
        generator_bids.loc[generator_bids["RESOURCEBID_SEQ"]==gen_id, "unitMW"]= test2

    for gen_id in set(generator_bids["RESOURCEBID_SEQ"][generator_bids["RESOURCE_TYPE"] == "INTERTIE"]):
        # gen_id = 101436
        bidding_curve = generator_bids[generator_bids["RESOURCEBID_SEQ"] == gen_id]
        test = pd.concat(
            [bidding_curve["SCH_BID_XAXISDATA"], bidding_curve["SCH_BID_XAXISDATA"].shift(1, fill_value=0)], axis=1)
        y_test = pd.concat(
            [bidding_curve["SCH_BID_Y1AXISDATA"], bidding_curve["SCH_BID_Y1AXISDATA"].shift(1, fill_value=0)], axis=1)
        y_test2 = y_test.iloc[:, 0] - y_test.iloc[:, 1]
        if sum(y_test2.iloc[1:]) >= 0:
            # k += 1
            test2 = test.iloc[:, 0] - test.iloc[:, 1]
            test2 = test2.apply(lambda x: max(0, x))
            generator_bids.loc[generator_bids["RESOURCEBID_SEQ"] == gen_id, "unitMW"] = test2

    generator_bids["bid_price"] = generator_bids['SCH_BID_Y1AXISDATA']
    generator_bids = generator_bids.sort_values(by='bid_price')
    generator_bids['cumsum_MW'] = generator_bids['unitMW'].cumsum()
    bids_not_ss = generator_bids[generator_bids["bid_price"].notna()]
    generator_bids['cumsum_MW'] += self_schedule_for_eight
    return generator_bids

# generator_bids = get_generator_bids(bids_for_eight)
#
# test_for_Sena = generator_bids[generator_bids["cumsum_MW"]<=105000]
# plt.figure(figsize=(10,8))
# plt.plot(test_for_Sena["cumsum_MW"], test_for_Sena["bid_price"])
# plt.title("Day ahead market bid prices for " + str(eight_hour_datetime))
# plt.xlabel("Cumulated MW")
# plt.ylabel("Bid price USD/MWh")
# plt.axhline(y=0, color="black")
# plt.axvline(x=0, color="black")
# plt.axhline(y=39.7, color="red", label="clearing price")
# # plt.axvline(x=load.iloc[7], label="Load of all zones in California", color="orange")
# # plt.axvline(x=float(load_CAISO[load_CAISO["OPR_HR"]==8]["MW"]), label="load CAISO")
# plt.grid(True)
# plt.legend()
# plt.show()


"""
Reconstruct demand
"""
def get_hour_load_curve(bids_for_eight):
    load_bids = bids_for_eight[bids_for_eight["RESOURCE_TYPE"].isin(["LOAD", "INTERTIE"])]
    # intertie_bids = bids_for_eight[bids_for_eight["RESOURCE_TYPE"].isin(["INTERTIE"])]

    self_schedule_loads_for_eight = sum(load_bids["SELFSCHEDMW"].dropna()) #+ sum(intertie_bids["SELFSCHEDMW"].dropna())
    load_bids = load_bids[(load_bids["SELFSCHEDMW"].isna())]
    # intertie_bids = intertie_bids[(intertie_bids["SELFSCHEDMW"].isna())]

    load_bids["unitMW"] = 0
    for gen_id in set(load_bids["RESOURCEBID_SEQ"][load_bids["RESOURCE_TYPE"]=="LOAD"]):
        # gen_id = 101767
        bidding_curve = load_bids[load_bids["RESOURCEBID_SEQ"] == gen_id]
        test = pd.concat([bidding_curve["SCH_BID_XAXISDATA"], bidding_curve["SCH_BID_XAXISDATA"].shift(1, fill_value=0)], axis=1)
        test2 = test.iloc[:,0] - test.iloc[:,1]
        test2 = test2.apply(lambda x : max(0,x))
        load_bids.loc[load_bids["RESOURCEBID_SEQ"]==gen_id, "unitMW"]= test2

    k = 0
    for gen_id in set(load_bids["RESOURCEBID_SEQ"][load_bids["RESOURCE_TYPE"]=="INTERTIE"]):
        # gen_id = 101436
        bidding_curve = load_bids[load_bids["RESOURCEBID_SEQ"] == gen_id]
        test = pd.concat(
            [bidding_curve["SCH_BID_XAXISDATA"], bidding_curve["SCH_BID_XAXISDATA"].shift(1, fill_value=0)], axis=1)
        y_test = pd.concat(
            [bidding_curve["SCH_BID_Y1AXISDATA"], bidding_curve["SCH_BID_Y1AXISDATA"].shift(1, fill_value=0)], axis=1)
        y_test2 = y_test.iloc[:, 0] - y_test.iloc[:, 1]
        if len(y_test2)>1:
            if sum(y_test2.iloc[1:]) < 0:
                k +=1
                test2 = test.iloc[:, 0] - test.iloc[:, 1]
                test2 = test2.apply(lambda x: max(0, x))
                load_bids.loc[load_bids["RESOURCEBID_SEQ"] == gen_id, "unitMW"] = test2
    # intertie_bids = load_bids[load_bids["RESOURCE_TYPE"].isin(["INTERTIE"])]
    # for gen_id in set(intertie_bids["RESOURCEBID_SEQ"]):
    #     # gen_id = 101767
    #     bidding_curve = intertie_bids[intertie_bids["RESOURCEBID_SEQ"] == gen_id]
    #     test = pd.concat([intertie_bids["SCH_BID_XAXISDATA"], intertie_bids["SCH_BID_XAXISDATA"].shift(1, fill_value=0)], axis=1)
    #     test2 = test.iloc[:,0] - test.iloc[:,1]
    #     test2 = test2.apply(lambda x : max(0,x))
    #     intertie_bids.loc[intertie_bids["RESOURCEBID_SEQ"]==gen_id, "unitMW"]= test2

    load_bids["bid_price"] = load_bids['SCH_BID_Y1AXISDATA']
    load_bids = load_bids.sort_values(by='bid_price', ascending=False)
    load_bids['cumsum_MW'] = load_bids['unitMW'].cumsum()
    # bids_not_ss = generator_bids[generator_bids["bid_price"].notna()]
    load_bids['cumsum_MW'] += self_schedule_loads_for_eight
    return load_bids

# load_bids = get_hour_load_curve(bids_for_eight)
# load_bids_2018 = get_hour_load_curve(bids_for_eight_2018)
#
#
# test_for_Sena = load_bids[load_bids["cumsum_MW"]<=105000]
# plt.figure(figsize=(10,8))
# plt.plot(test_for_Sena["cumsum_MW"], test_for_Sena["bid_price"])
# plt.title("Day ahead market bid prices for " + str(eight_hour_datetime))
# plt.xlabel("Cumulated MW")
# plt.ylabel("Bid price USD/MWh")
# plt.axhline(y=0, color="black")
# plt.axvline(x=0, color="black")
# plt.axhline(y=39.7, color="red", label="clearing price")
# # plt.axvline(x=load.iloc[7], label="Load of all zones in California", color="orange")
# # plt.axvline(x=float(load_CAISO[load_CAISO["OPR_HR"]==8]["MW"]), label="load CAISO")
# plt.grid(True)
# plt.legend()
# plt.show()


"""
Full example 
"""
# import intersect
# x1 = load_bids["cumsum_MW"].values
# y1 = load_bids["bid_price"].values
# x3 = load_bids_2018["cumsum_MW"].values
# y3 = load_bids_2018["bid_price"].values
# x2 = generator_bids["cumsum_MW"].values
# y2 = generator_bids["bid_price"].values
# x_2019, y_2019 = intersect.intersection(x1, y1, x2, y2)
# x_2018, y_2018 = intersect.intersection(x3, y3, x2, y2)


# test_for_Sena = generator_bids[generator_bids["cumsum_MW"]<=105000]
def plot_results(eight_hour_datetime, generator_bids, load_bids, load_bids_2018, x_2019, y_2019, x_2018, y_2018):
    plt.figure(figsize=(10,8))
    plt.plot(generator_bids["cumsum_MW"], generator_bids["bid_price"], label="Supply curve")
    plt.plot(load_bids["cumsum_MW"], load_bids["bid_price"], label="Demand curve")
    plt.plot(load_bids_2018["cumsum_MW"], load_bids_2018["bid_price"], label="2018 Demand curve")
    plt.title("Day ahead market bid prices for " + str(eight_hour_datetime))
    plt.xlabel("Cumulated MW")
    plt.ylabel("Bid price USD/MWh")
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    # plt.axhline(y=y_2019[0], color="C1", label="Actual clearing price : \${}".format(y_2019[0]))
    # plt.axvline(x=x_2019[0], color="C2", label="Actual cleared volume : {}GWh".format(x_2019[0]))
    # plt.axhline(y=y_2018[0], color="C3", label="clearing price with 2018 load : \${}".format(y_2018[0]))
    # plt.axvline(x=x_2018[0], color="C4", label="cleared volume with 2018 load : {}GWh".format(x_2018[0]))
    #
    # """
    # Fill between
    # """
    # x = generator_bids["cumsum_MW"][(generator_bids["cumsum_MW"]>=x_2019[0])& (generator_bids["cumsum_MW"]<=x_2018[0])]
    # y_1 = [y_2019[0]]*len(x)
    # y_2 = generator_bids["bid_price"][(generator_bids["cumsum_MW"]>=x_2019[0])& (generator_bids["cumsum_MW"]<=x_2018[0])]
    # plt.fill_between(x, y_1, y_2, where=(y_1 < y_2), alpha=0.5, color="yellow")
    # plt.axvline(x=load.iloc[7], label="Load of all zones in California", color="orange")
    # plt.axvline(x=float(load_CAISO[load_CAISO["OPR_HR"]==8]["MW"]), label="load CAISO")
    # plt.xlim(30000,50000)
    # plt.ylim(-10,100)
    plt.grid(True)
    plt.legend()
    plt.show()

# plot_results(generator_bids, load_bids, load_bids_2018, x_2019, y_2019, x_2018, y_2018)

# import numpy as np
# calculus_df = pd.DataFrame()
# calculus_df["x"] = x
# calculus_df["diffy"] = y_2-y_1
# calculus_df["dx"] = calculus_df["x"] - calculus_df["x"].shift(1)
# surplus = np.nansum(calculus_df["dx"]*calculus_df["diffy"])

def lost_surplus(df, df_2018, hour=8, plot=False):
    date = df["start_date"].iloc[0]
    eight_hour_datetime = datetime.datetime(date.year, date.month, date.day, hour)


    date_2018 = df_2018["start_date"].iloc[0]
    eight_hour_datetime_2018 = datetime.datetime(date_2018.year, date_2018.month, date_2018.day, hour)
    bids_for_eight = df[(df["start_date"] <= eight_hour_datetime) & (
                df["end_date"] >= eight_hour_datetime + datetime.timedelta(hours=1))]
    bids_for_eight_2018 = df_2018[(df_2018["start_date"] <= eight_hour_datetime_2018) & (
                df_2018["end_date"] >= eight_hour_datetime_2018 + datetime.timedelta(hours=1))]

    load_bids = get_hour_load_curve(bids_for_eight)
    load_bids_2018 = get_hour_load_curve(bids_for_eight_2018)
    generator_bids = get_generator_bids(bids_for_eight)

    x1 = load_bids["cumsum_MW"].values
    y1 = load_bids["bid_price"].values
    x3 = load_bids_2018["cumsum_MW"].values
    y3 = load_bids_2018["bid_price"].values
    x2 = generator_bids["cumsum_MW"].values
    y2 = generator_bids["bid_price"].values
    x_2019, y_2019 = intersect.intersection(x1, y1, x2, y2)
    x_2018, y_2018 = intersect.intersection(x3, y3, x2, y2)

    if plot:
        plot_results(eight_hour_datetime, generator_bids, load_bids, load_bids_2018, x_2019, y_2019, x_2018, y_2018)

    if x_2019[0] <= x_2018[0]:
        x = generator_bids["cumsum_MW"][
            (generator_bids["cumsum_MW"] >= x_2019[0]) & (generator_bids["cumsum_MW"] <= x_2018[0])]
        y_1 = [y_2019[0]] * len(x)
        y_2 = generator_bids["bid_price"][
            (generator_bids["cumsum_MW"] >= x_2019[0]) & (generator_bids["cumsum_MW"] <= x_2018[0])]
    else:
        x = generator_bids["cumsum_MW"][
            (generator_bids["cumsum_MW"] <= x_2019[0]) & (generator_bids["cumsum_MW"] >= x_2018[0])]
        y_1 = [y_2018[0]] * len(x)
        y_2 = generator_bids["bid_price"][
            (generator_bids["cumsum_MW"] <= x_2019[0]) & (generator_bids["cumsum_MW"] >= x_2018[0])]

    calculus_df = pd.DataFrame()
    calculus_df["x"] = x
    calculus_df["diffy"] = y_2 - y_1
    calculus_df["dx"] = calculus_df["x"] - calculus_df["x"].shift(1)
    surplus = np.nansum(calculus_df["dx"] * calculus_df["diffy"])
    if x_2019[0] >= x_2018[0]:
        surplus = -surplus

    return surplus, (x_2019[0], y_2019[0]), (x_2018[0], y_2018[0])

def run_test():
    # final_test = lost_surplus(df, df_2018, hour=18, plot=False)
    # index = pd.date_range(datetime.datetime(2019,10,10), datetime.datetime(2019,10,11), freq="H")
    # result_df = pd.DataFrame(index=index, columns=["Lost Surplus", "actual cleared volume", "actual cleared price",
    #                                                "expected cleared volume", "expected cleared price"])
    # for date in index:
    #     hour = date.hour
    #     if hour <= 23:
    #         print(hour)
    #         data = lost_surplus(df, df_2018, hour=hour, plot=False)
    #         result_df.loc[date] = [data[0], data[1][0], data[1][1], data[2][0], data[2][1]]


    starting_date = datetime.date(2019,10,8)
    return_df = pd.DataFrame()
    i = 0
    while i < 25:
        i += 1
        try:
            print("----"*20)
            starting_date = starting_date + datetime.timedelta(days=1)
            str_date = starting_date.strftime("%Y%m%d")
            str_date_2018 = (starting_date - datetime.timedelta(days=364)).strftime("%Y%m%d")
            print(str_date + " and " + str_date_2018)
            df = pd.read_csv("data/public_bids/{}_{}_PUB_BID_DAM_v2.csv".format(str_date, str_date))
            df_2018 = pd.read_csv("data/public_bids/{}_{}_PUB_BID_DAM_v2.csv".format(str_date_2018, str_date_2018))
            test = df.describe()
            df = treat_df(df)
            df_2018 = treat_df(df_2018)

            index = pd.date_range(starting_date, starting_date + datetime.timedelta(days=1), freq="H")[:-1]
            result_df = pd.DataFrame(index=index, columns=["Lost Surplus", "actual cleared volume", "actual cleared price",
                                                           "expected cleared volume", "expected cleared price"])
            for date in index:
                hour = date.hour
                if hour <= 23:
                    print(hour)
                    data = lost_surplus(df, df_2018, hour=hour, plot=False)
                    result_df.loc[date] = [data[0], data[1][0], data[1][1], data[2][0], data[2][1]]

            return_df = pd.concat([return_df, result_df])
            print("----" * 20)
            print("\n")
        except:
            break

    return_df.to_csv("results2.csv")

    pd.plotting.register_matplotlib_converters()
    plt.figure(figsize=(10,8))
    # plt.axhline(y=0, color="black")
    plt.plot(return_df.index, return_df["Lost Surplus"]) #, label="Lost Surplus")
    # plt.title("Expected lost surplus for generators from {} to {} ".format(str(return_df.index[0].date()),
    #                                                                        str(return_df.index[-1].date())))
    plt.legend()
    plt.show()

    return_df["start_date"] = return_df.index
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    fig, ax = plt.subplots(figsize=(15, 8))

    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    # rotate and align the tick labels so they look better
    plt.plot(return_df["start_date"].iloc[:10], return_df["Lost Surplus"].iloc[:10])
    fig.autofmt_xdate()
    plt.legend()
    plt.show()

    # plt.plot(generator_bids["cumsum_MW"], generator_bids["bid_price"], label="Supply curve")
    # plt.plot(load_bids["cumsum_MW"], load_bids["bid_price"], label="Demand curve")
    # plt.plot(load_bids_2018["cumsum_MW"], load_bids_2018["bid_price"], label="2018 Demand curve")
    # plt.title("Day ahead market bid prices for " + str(eight_hour_datetime))
    # plt.xlabel("Cumulated MW")
    # plt.ylabel("Bid price USD/MWh")
    # plt.axhline(y=0, color="black")
    # plt.axvline(x=0, color="black")
    # plt.axhline(y=y_2019[0], color="C1", label="Actual clearing price : \${}".format(y_2019[0]))
    # plt.axvline(x=x_2019[0], color="C2", label="Actual cleared volume : {}GWh".format(x_2019[0]))
    # plt.axhline(y=y_2018[0], color="C3", label="clearing price with 2018 load : \${}".format(y_2018[0]))
    # plt.axvline(x=x_2018[0], color="C4", label="cleared volume with 2018 load : {}GWh".format(x_2018[0]))

    """
    Fill between 
    """
    # x = generator_bids["cumsum_MW"][(generator_bids["cumsum_MW"]>=x_2019[0])& (generator_bids["cumsum_MW"]<=x_2018[0])]
    # y_1 = [y_2019[0]]*len(x)
    # y_2 = generator_bids["bid_price"][(generator_bids["cumsum_MW"]>=x_2019[0])& (generator_bids["cumsum_MW"]<=x_2018[0])]
    # plt.fill_between(x, y_1, y_2, where=(y_1 < y_2), alpha=0.5, color="yellow")
    # # plt.axvline(x=load.iloc[7], label="Load of all zones in California", color="orange")
    # # plt.axvline(x=float(load_CAISO[load_CAISO["OPR_HR"]==8]["MW"]), label="load CAISO")
    # plt.xlim(30000,50000)
    # plt.ylim(-10,100)
    plt.grid(True)
    plt.legend()
    plt.show()