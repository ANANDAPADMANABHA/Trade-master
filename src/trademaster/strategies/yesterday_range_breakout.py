import datetime as dt
import time
from typing import List

import pandas as pd
from broker import AngelOneClient
from utils import token_lookup


class YesterdayRangeBreakout(AngelOneClient):
    def range_breakout(
        self, tickers: List[str], exchange: str = 'NSE'
    ) -> None:
        for ticker in tickers:
            time.sleep(0.4)
            params = {
                'exchange': exchange,
                'symboltoken': token_lookup(ticker, self.instrument_list),
                'interval': 'ONE_DAY',
                'fromdate': (dt.date.today() - dt.timedelta(1)).strftime(
                    '%Y-%m-%d %H:%M'
                ),
                'todate': dt.datetime.now().strftime('%Y-%m-%d %H:%M'),
            }
            try:
                hist_data = self.smart_api.getCandleData(params)
                df_data = pd.DataFrame(
                    hist_data['data'],
                    columns=['date', 'open', 'high', 'low', 'close', 'volume'],
                )
                df_data['high'].tolist()
            except Exception as e:
                print(e)
