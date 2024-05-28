import time
import pandas as pd
import datetime as dt
from src.trademaster.data_loader import ORB_TICKERS
from src.trademaster.strategies.opening_range_breakout import OpeningRangeBreakout

class TradeMaster(OpeningRangeBreakout):
    def make_some_money(self) -> None:
            print('Lets make some money')
            starttime = time.time()
            hi_lo_prices = {}
            self._load_instrument_list()
            self._initialize_smart_api()
            data_0920 = self.hist_data_0920(
                ORB_TICKERS, 4, "FIVE_MINUTE", self.instrument_list)
            for ticker in ORB_TICKERS:
                hi_lo_prices[ticker] = [data_0920[ticker]["high"].iloc[-1], data_0920[ticker]["low"].iloc[-1]]
            df = pd.DataFrame.from_dict(hi_lo_prices)
            print(df)

            while dt.datetime.now() < dt.datetime.strptime(dt.datetime.now().strftime('%Y-%m-%d')+' 15:30', '%Y-%m-%d %H:%M'):
                print("starting passthrough at {}".format(dt.datetime.now()))
                positions = pd.DataFrame(self.smart_api.position()["data"])
                open_orders = self.get_open_orders()
                self.orb_strat(ORB_TICKERS, hi_lo_prices, positions, open_orders)
                time.sleep(300 - ((time.time() - starttime) % 300.0))
                
trade = TradeMaster()
trade.make_some_money()