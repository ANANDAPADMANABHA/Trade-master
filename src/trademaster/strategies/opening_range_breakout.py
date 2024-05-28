import json
import time
import datetime as dt
from typing import List, Dict, Union, Optional, Tuple
from src.trademaster.utils import token_lookup
import pandas as pd

from src.trademaster.broker import AngelOneClient

class OpeningRangeBreakout(AngelOneClient):
    """A class to implement Opening Range Breakout trading strategy."""
    # Access environment variables
              
    def orb_strat(self, tickers: List[str], hi_lo_prices: Dict[str, List[float]], positions: pd.DataFrame, open_orders: Optional[pd.DataFrame] = None, exchange: str = "NSE") -> None:
        """
        Implements an Opening Range Breakout (ORB) strategy for given tickers.

        Args:
            tickers (List[str]): List of ticker symbols to analyze.
            hi_lo_prices (Dict[str, List[float]]): Dictionary containing high and low prices for each ticker.
            positions (pd.DataFrame): DataFrame containing current positions.
            open_orders (Optional[pd.DataFrame], optional): DataFrame containing open orders. Defaults to None.
            exchange (str, optional): Name of the exchange. Defaults to "NSE".

        Returns:
            None
        """
        quantity = 1
        if not positions.empty:
            tickers = [i for i in tickers if i +
                       "-EQ" not in positions["tradingsymbol"].to_list()]
        if not open_orders.empty:
            tickers = [i for i in tickers if i +
                       "-EQ" not in open_orders["tradingsymbol"].to_list()]

        for ticker in tickers:
            time.sleep(0.4)
            params = {
                "exchange": exchange,
                "symboltoken": token_lookup('WIPRO', self.instrument_list),
                "interval": "FIVE_MINUTE",
                "fromdate": (dt.date.today() - dt.timedelta(4)).strftime('%Y-%m-%d %H:%M'),
                "todate": dt.datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            try:
                hist_data = self.smart_api.getCandleData(params)
                df_data = pd.DataFrame(hist_data["data"], columns=[
                                       "date", "open", "high", "low", "close", "volume"])
                df_data.set_index("date", inplace=True)
                df_data.index = pd.to_datetime(df_data.index)
                df_data.index = df_data.index.tz_localize(None)
                df_data["avg_vol"] = df_data["volume"].rolling(
                    10).mean().shift(1)
                if df_data["volume"].iloc[-1] >= df_data["avg_vol"].iloc[-1]:
                    print('ALERT..............!')
                    print(f'{ticker} has broken the average volume')
                    if df_data["close"].iloc[-1] >= hi_lo_prices[ticker][0] and df_data["low"].iloc[-1] >= hi_lo_prices[ticker][1]:
                        self.place_robo_order(
                            self.instrument_list, ticker, "BUY", hi_lo_prices[ticker], quantity)
                        print(f"Bought {quantity} stocks of {ticker}")
                    elif df_data["close"].iloc[-1] <= hi_lo_prices[ticker][0] and df_data["high"].iloc[-1] <= hi_lo_prices[ticker][1]:
                        self.place_robo_order(
                            self.instrument_list, ticker, "SELL", hi_lo_prices[ticker], quantity)
                        print("sold {} stocks of {}".format(quantity, ticker))
                else:
                    print(f'NO TRADE : {ticker}')
            except Exception as e:
                print(e)
            
    
