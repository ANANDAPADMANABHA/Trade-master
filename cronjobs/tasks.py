from celery import shared_task

from src.trademaster.trading_bot import TradeMaster


@shared_task
def run_trade_task():
    trade = TradeMaster()
    trade.make_some_money()
