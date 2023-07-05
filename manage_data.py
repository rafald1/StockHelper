import os
import datetime as dt
import pandas as pd
from pandas_datareader import data

from gpw_tickers import tickers


class Stock:
    def __init__(self):
        self.df_original = None
        self.df = None

    def read_stock_data_from_file(self):
        self.df_original = pd.read_csv("data/gpw_stock_data.csv", header=[0, 1], index_col=0)
        self.df_original.index = pd.to_datetime(self.df_original.index)

    def fetch_new_data_and_update(self, start_date, end_date):
        tickers_lst = list(tickers.keys())
        new_stock_data = data.DataReader(name=tickers_lst, data_source="stooq", start=start_date, end=end_date)
        # TODO: check the size of fetched data. It should have 1850 columns.
        pd.DataFrame.to_csv(new_stock_data, "data/new_gpw_stock_data.csv")

        self.df_original = pd.concat(objs=[self.df_original, new_stock_data]).drop_duplicates()
        self.df_original = self.df_original.sort_index(ascending=True)

    def write_stock_date_to_file(self):
        now = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename("data/gpw_stock_data.csv", f"data/{now}_gpw_stock_data.csv")
        pd.DataFrame.to_csv(self.df_original, "data/gpw_stock_data.csv")

    def prepare_data(self, start_date, end_date, missing_data_percentage_cutoff):
        self.df = self.df_original.loc[start_date:end_date].copy()

        # Count the number of missing values
        mask = self.df["Close"].isna().sum()

        # Create a list with stock names that missing value percentage is higher than specified
        lst = list(mask[mask > len(self.df.index) * missing_data_percentage_cutoff / 100].to_dict().keys())

        # Drop columns with stock values that missing value percentage is higher than specified
        for name in lst:
            self.df.drop([("Close", name), ("High", name), ("Low", name), ("Open", name), ("Volume", name)],
                         axis=1, inplace=True)

        # Replace NaN with 0 for Volume and with previous value for Close nad Open values
        self.df["Volume"] = self.df["Volume"].fillna(0)
        self.df["Close"] = self.df["Close"].fillna(method="ffill")
        self.df["Open"] = self.df["Open"].fillna(method="ffill")
        print(self.df.shape)
