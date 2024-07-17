import datetime as dt
import json
import os
import time
import urllib
from typing import Dict, List, Optional, Union

import pandas as pd
from pyotp import TOTP
from SmartApi import SmartConnect

from src.trademaster.utils import token_lookup


class AngelOneClient:
    def __init__(self) -> None:
        self.api_key: str = os.environ.get('API_KEY')
        self.client_id: str = os.environ.get('CLIENT_ID')
        self.password: str = os.environ.get('PASSWORD')
        self.token: str = os.environ.get('TOKEN')
        self.totp: str = TOTP(self.token).now()
        self.smart_api = None
        self.instrument_list = None

    def _initialize_smart_api(self) -> None:
        """Initialize the SmartAPI session."""
        if self.smart_api is None:
            self.smart_api = SmartConnect(self.api_key)
            self.smart_api.generateSession(
                self.client_id, self.password, self.totp
            )

    def _load_instrument_list(self) -> None:
        """Load the instrument list."""
        if self.instrument_list is None:
            instrument_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
            response = urllib.request.urlopen(instrument_url)
            self.instrument_list: List[
                Dict[str, Union[str, int]]
            ] = json.loads(response.read())

    def quantity(self, ticker: str, exchange: str = 'NSE') -> int:
        """Calculate the quantity of stocks to buy/sell."""
        pos_size: int = 500
        ltp: Optional[float] = self.get_ltp(
            self.instrument_list, ticker, exchange
        )
        if ltp:
            return int(pos_size / ltp)
        return 0

    def get_ltp(
        self,
        instrument_list: List[Dict[str, Union[str, int]]],
        ticker: str,
        exchange: str = 'NSE',
    ) -> Optional[float]:
        """Get the Last Traded Price (LTP) of a given ticker."""
        params: Dict[str, Union[str, int]] = {
            'tradingsymbol': '{}-EQ'.format(ticker),
            'symboltoken': token_lookup(ticker, instrument_list),
        }
        try:
            response = self.smart_api.ltpData(
                exchange, params['tradingsymbol'], params['symboltoken']
            )
            if response:
                return response['data']['ltp']
        except Exception as e:
            print(f'Exception getltp {e}')
        return None

    def place_robo_order(
        self,
        instrument_list: List[Dict[str, Union[str, int]]],
        ticker: str,
        buy_sell: str,
        prices: List[float],
        quantity: int,
        exchange: str = 'NSE',
    ) -> Optional[Dict[str, Union[str, int]]]:
        """Place a robo order."""
        ltp: Optional[float] = self.get_ltp(instrument_list, ticker, exchange)
        if not ltp:
            return None
        params: Dict[str, Union[str, int, float]] = {
            'variety': 'ROBO',
            'tradingsymbol': '{}-EQ'.format(ticker),
            'symboltoken': token_lookup(ticker, instrument_list),
            'transactiontype': buy_sell,
            'exchange': exchange,
            'ordertype': 'LIMIT',
            'producttype': 'BO',
            'price': ltp ,
            'duration': 'DAY',
            'stoploss': round(ltp * 0.01, 1), 
            'squareoff': round(ltp * 0.01, 1),
            'quantity': quantity,
        }
        try:
            response = self.smart_api.placeOrder(params)
            return response
        except Exception as e:
            print(e)
            return None

    def get_open_orders(self) -> Optional[pd.DataFrame]:
        """Retrieve open orders."""
        try:
            response = self.smart_api.orderBook()
            df: pd.DataFrame = pd.DataFrame(response['data'])
            if len(df) > 0:
                return df[df['orderstatus'] == 'open']
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def hist_data_0920(
        self,
        tickers: List[str],
        duration: int,
        interval: str,
        instrument_list: List[Dict[str, Union[str, int]]],
        exchange: str = 'NSE',
    ) -> Dict[str, pd.DataFrame]:
        """Get historical data at 9:20 am."""
        hist_data_tickers: Dict[str, pd.DataFrame] = {}
        for ticker in tickers:
            time.sleep(0.4)
            params: Dict[str, Union[str, int]] = {
                'exchange': exchange,
                'symboltoken': token_lookup(ticker, instrument_list),
                'interval': interval,
                'fromdate': (
                    dt.date.today() - dt.timedelta(duration)
                ).strftime('%Y-%m-%d %H:%M'),
                'todate': dt.date.today().strftime('%Y-%m-%d') + ' 09:19',
            }
            try:
                hist_data = self.smart_api.getCandleData(params)
                df_data: pd.DataFrame = pd.DataFrame(
                    hist_data['data'],
                    columns=['date', 'open', 'high', 'low', 'close', 'volume'],
                )
                df_data.set_index('date', inplace=True)
                df_data.index = pd.to_datetime(df_data.index)
                df_data.index = df_data.index.tz_localize(None)
                df_data['gap'] = (
                    (df_data['open'] / df_data['close'].shift(1)) - 1
                ) * 100
                hist_data_tickers[ticker] = df_data
            except Exception as e:
                print(e)
        return hist_data_tickers
