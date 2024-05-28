from src.trademaster.trading_bot import TradeMaster
from celery import shared_task

@shared_task
def run_trade_task():
    trade = TradeMaster()
    trade.make_some_money()

