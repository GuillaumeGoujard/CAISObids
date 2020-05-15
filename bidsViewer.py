import pandas as pd

df = pd.read_csv("data/20191010_20191010_PUB_BID_DAM_v2.csv")
test = df.describe()
df.columns

# df = pd.read_csv("data/20200209_20200209_PUB_BID_RTM_v2.csv")

sum(df["SCH_BID_XAXISDATA"].dropna())

df = df[df["RESOURCE_TYPE"] == "GENERATOR"]
df = df[df["MARKETPRODUCTTYPE"]=="EN"]
df["start_date"] = pd.to_datetime(df["TIMEINTERVALSTART"])
df["end_date"] = pd.to_datetime(df["TIMEINTERVALEND"])
bids_time_treated = pd.to_datetime(df["SCH_BID_TIMEINTERVALSTART"]).dropna()
df.loc[bids_time_treated.index, "start_date"] = bids_time_treated
bids_time_treated = pd.to_datetime(df["SCH_BID_TIMEINTERVALSTOP"]).dropna()
df.loc[bids_time_treated.index, "end_date"] = bids_time_treated

test = df[df["SCH_BID_Y1AXISDATA"]==0]
df = df.drop_duplicates()
test = df[df["SCH_BID_Y1AXISDATA"]>=1000]
df["self_schedule"] = df["SELFSCHEDMW"]
df["bid_price"] = df["SCH_BID_Y1AXISDATA"]
df["bid_volume"] = df["SCH_BID_XAXISDATA"]
cleaned_df = df
cleaned_df = df[["start_date","end_date", "self_schedule", "bid_price", "bid_volume"]]
cleaned_df = cleaned_df[cleaned_df['start_date'].notna()]
cleaned_df["start_hour"] = cleaned_df["start_date"].apply(lambda s: s.hour)
cleaned_df["end_hour"] = cleaned_df["end_date"].apply(lambda s: s.hour)

date = cleaned_df["start_date"].iloc[0]
import datetime
eight_hour_datetime = datetime.datetime(date.year, date.month, date.day, 8)

bids_for_eight = cleaned_df[(cleaned_df["start_date"]>=eight_hour_datetime) & (cleaned_df["end_date"]<=eight_hour_datetime+datetime.timedelta(hours=1))]
self_schedule_for_eight = sum(bids_for_eight["self_schedule"].dropna())
bids_for_eight = bids_for_eight.sort_values(by='bid_price')
bids_for_eight['cumsum_MW'] = bids_for_eight['bid_volume'].cumsum()
bids_not_ss = bids_for_eight[bids_for_eight["bid_price"].notna()]
bids_for_eight['cumsum_MW'] += self_schedule_for_eight
import matplotlib.pyplot as plt

test_for_Sena = bids_for_eight[bids_for_eight["cumsum_MW"]<=60000]
plt.figure(figsize=(10,8))
plt.plot(test_for_Sena["cumsum_MW"], test_for_Sena["bid_price"])
plt.title("Day ahead market bid prices for " + str(eight_hour_datetime))
plt.xlabel("Cumulated MW")
plt.ylabel("Bid price USD/MWh")
plt.axhline(y=0, color="black")
plt.axvline(x=0, color="black")
plt.axhline(y=39.7, color="red", label="clearing price")
plt.axvline(x=load.iloc[7], label="Load of all zones in California", color="orange")
plt.axvline(x=float(load_CAISO[load_CAISO["OPR_HR"]==8]["MW"]), label="load CAISO")
plt.grid(True)
plt.legend()
plt.show()

demand = pd.read_csv("data/CAISO-demand-20191010.csv").T
hour = 8
demand["hour"] = demand.index
demand["hour"].apply(lambda s : s[:2])
demand.iloc[hour*13:(hour+1)*13+1]

demand = pd.read_csv("data/20191010_20191011_ENE_SLRS_DAM_20200511_12_10_51_v1.csv")

load = demand[demand["SCHEDULE"]=="Load"].groupby("OPR_HR").sum()["MW"]
load_CAISO = demand[(demand["SCHEDULE"]=="Load") & (demand["TAC_ZONE_NAME"]=="Caiso_Totals")]
set(demand["TAC_ZONE_NAME"])

# test = bids_not_ss.groupby('MARKETPRODUCTTYPE').sum()
#
# cleared_prices = pd.read_csv("data/20191010_20191010_PRC_LMP_DAM_20200510_10_53_51_v1.csv")
# test = cleared_prices[(cleared_prices["OPR_HR"]==8)&(cleared_prices["XML_DATA_ITEM"]=="LMP_ENE_PRC")]
# lmp = pd.unique(test["MW"])[0]