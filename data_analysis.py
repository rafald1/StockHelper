import pandas as pd
import numpy as np

from gpw_tickers import tickers


class Analysis:
    def __init__(self, dataframe):
        self.df = dataframe

    @staticmethod
    def _append_name_and_url_columns(df, chart_type="l"):
        """
        Adds full name and url columns
        chart_type:
        l - line
        c - candle
        """
        # Add a new column and replace values based on the dictionary to convert tickers to full company names
        df.insert(0, "Name", df.index)
        df.replace({"Name": tickers}, inplace=True)

        df["url"] = "https://stooq.pl/q/a2/?s=" + df.index.str[:-3].str.lower()\
                    + "&i=d&t=" + chart_type + "&a=ln&z=231&ft=20220222&l=127&d=1&ch=0&f=1&lt=57&r=0&o=1"

        return df

    def stock_price_pct_change(self, no_of_sessions, pct_decrease, pct_increase):
        ptc_change = self.df.iloc[-no_of_sessions - 1:]["Close"].pct_change(periods=no_of_sessions) * 100
        result = ptc_change.iloc[-1].squeeze()
        result = result[(result < pct_decrease) | (result > pct_increase)].sort_values()

        df_result = pd.DataFrame(result)
        df_result.columns = ["Percentage Change"]
        df_result = self._append_name_and_url_columns(df_result, chart_type="l")

        return df_result.to_string()

    def looking_for_gaps(self, pct_change=5, session_shift=0):
        open_value = self.df.iloc[-session_shift - 1]["Open"]
        close_value = self.df.iloc[-session_shift - 2]["Close"]
        result = (open_value - close_value) / close_value * 100
        result = result[(result < -pct_change) | (result > pct_change)].sort_values()

        for element in result.index:
            if result[element] > 0:
                if self.df.iloc[-session_shift - 1][("Low", element)] < close_value[element]:
                    result.drop(element)
                    print(f"Dropped {element}")
            else:
                if self.df.iloc[-session_shift - 1][("High", element)] > close_value[element]:
                    result.drop(element)
                    print(f"Dropped {element}")

        df_result = pd.DataFrame(result)
        df_result.columns = ["Percentage Gap"]
        df_result = self._append_name_and_url_columns(df_result, chart_type="c")
        return df_result.to_string()

    def calculate_macd(self, pct_distance=1, session_shift=0):
        """
        MACD (12, 26, 9)
        :param pct_distance:
        :param session_shift: 0 = last session, x = session that occurred x sessions ago
        :return:
        """
        # Calculate MACD and Signal
        ema_12 = self.df["Close"].ewm(span=12, adjust=False).mean()
        ema_26 = self.df["Close"].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()

        # Calculate spread of MACD
        distance_percentage = (signal - macd) / (macd.max() - macd.min()) * 100
        result = distance_percentage.iloc[-session_shift - 1].squeeze()
        result = result[abs(result) <= pct_distance]

        df_result = pd.DataFrame(result)
        df_result.columns = ["MACD diff [%]"]
        df_result = self._append_name_and_url_columns(df_result, chart_type="l")

        return df_result.to_string()

    def calculate_rsi(self, low_rsi, high_rsi, periods=14, session_shift=0):
        """
        RSI
        :param low_rsi:
        :param high_rsi:
        :param periods:
        :param session_shift: 0 = last session, x = session that occurred x sessions ago
        :return:
        """
        stock_close_diff = self.df["Close"].diff()
        up = stock_close_diff.clip(lower=0)
        down = -1 * stock_close_diff.clip(upper=0)
        ema_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ema_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        rsi = ema_up / ema_down
        rsi = 100 - (100 / (1 + rsi))

        result = rsi.iloc[-session_shift - 1].squeeze()
        result = result[(result < low_rsi) | (result > high_rsi)].sort_values()

        df_result = pd.DataFrame(result)
        df_result.columns = ["RSI value"]
        df_result = self._append_name_and_url_columns(df_result, chart_type="l")

        return df_result.to_string()

    def calculate_adx(self, period=14, session_shift=0):
        # TR
        h_l_diff = self.df['High'] - self.df['Low']
        h_pc_diff = abs(self.df['High'] - self.df['Close'].shift(1))
        l_pc_diff = abs(self.df['Low'] - self.df['Close'].shift(1))
        tr = pd.concat([h_l_diff, h_pc_diff, l_pc_diff], keys=["h_l", "h_pc", "l_pc"]).groupby(level=1).max()

        # Average True Range (ATR)
        atr = tr.ewm(alpha=1 / period, adjust=False).mean()

        # +DX, -DX
        h_diff = self.df["High"].diff()
        l_diff = self.df['Low'].shift(1) - self.df['Low']
        p_dm = pd.DataFrame(np.where((h_diff > l_diff) & (h_diff > 0), h_diff, 0), columns=h_diff.columns,
                            index=h_diff.index)
        n_dm = pd.DataFrame(np.where((l_diff > h_diff) & (l_diff > 0), l_diff, 0), columns=h_diff.columns,
                            index=h_diff.index)
        s_p_dm = p_dm.ewm(alpha=1/period, adjust=False).mean()
        s_n_dm = n_dm.ewm(alpha=1/period, adjust=False).mean()
        p_dmi = (s_p_dm / atr) * 100
        n_dmi = (s_n_dm / atr) * 100

        # ADX
        dx = (abs(p_dmi - n_dmi) / (p_dmi + n_dmi)) * 100
        adx = dx.ewm(alpha=1/period, adjust=False).mean()

        penultimate_session = adx.iloc[-2 - session_shift].squeeze()
        last_session = adx.iloc[-1 - session_shift].squeeze()
        mask = (penultimate_session <= 20) & (last_session > 20)
        result = last_session[mask].sort_values()

        # result = adx.iloc[-session_shift - 1].squeeze()
        # result = result[result > 25].sort_values()

        df_result = pd.DataFrame(result)
        df_result.columns = ["ADX value"]
        df_result = self._append_name_and_url_columns(df_result, chart_type="l")
        df_result.insert(2, "+DM", p_dmi.iloc[-1].squeeze())
        df_result.insert(3, "-DM", n_dmi.iloc[-1].squeeze())

        return df_result.to_string()
