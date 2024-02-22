from binance_historical_data import BinanceDataDumper
from datetime import datetime
data_dumper = BinanceDataDumper(
    path_dir_where_to_dump="D:\\Major_1\\test\\",
    asset_class="spot",  # spot, um, cm
    data_type="klines",  # aggTrades, klines, trades
    data_frequency="1h",
)
data_dumper.dump_data(
    tickers="BTCUSDT",
    date_start= datetime.date(year=2023, month=5, day=18),
    date_end= datetime.date(year=2023, month=10, day=24),
    is_to_update_existing=False,
    tickers_to_exclude=None,
)
data_dumper.dump_data()