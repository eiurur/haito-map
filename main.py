import pprint
import pandas as pd
import os
import datetime
import json
import yfinance as yf
from yahooquery import Ticker


read_file = pd.read_excel(r"tosho.xls")
read_file.to_csv(r"tosho.csv", index = None, header=False)

codes = pd.read_csv(r"tosho.csv", usecols=[1,2,3])
stock_tickers = [f"{row[1]}.T" for row in codes.itertuples()]
stock_names = [f"{row[2]}" for row in codes.itertuples()]
stock_segments = [f"{row[3]}" for row in codes.itertuples()]

today = datetime.date.today()
today_yyyymmdd = today.strftime('%Y%m%d')
db_dpath = f"./db/{today_yyyymmdd}"
os.makedirs(db_dpath, exist_ok=True)

# dump tickers
tickers_fpath = os.path.join(db_dpath, f"tickers.json")

sd = None
if os.path.exists(tickers_fpath):
    with open(tickers_fpath, 'r', encoding='utf-8') as f:
        sd = json.load(f)
else:
    tickers = Ticker(stock_tickers, progress=True)
    sd = tickers.summary_detail
    with open(tickers_fpath, 'w', encoding="utf-8") as f:
        json.dump(sd, f, indent = 4, ensure_ascii=False)

# dump stocks
stocks_provide_dividend = [] 
for idx, (ticker, detail) in enumerate(sd.items()):
    if "trailingAnnualDividendYield" not in detail or "trailingPE" not in detail:
        continue
    if detail["trailingAnnualDividendYield"] < 0.03:
        continue
    if detail["trailingPE"] < 25:
        continue

    name = stock_names[idx]
    segment = stock_segments[idx]
    stocks_provide_dividend.append({
      "ticker": ticker,
      "name": name,
      "segment": segment,
    })

print(len(stocks_provide_dividend))
data = [] 
for idx, stock in enumerate(stocks_provide_dividend):
    ticker_info = yf.Ticker(stock["ticker"])
    if "lastDividendValue" not in ticker_info.info or ticker_info.info["lastDividendValue"] is None:
        continue
    
    dividendRate = ticker_info.info["lastDividendValue"] / ticker_info.info["regularMarketPrice"]
    dividendYield = ticker_info.info["lastDividendValue"]
    previousClose = ticker_info.info["previousClose"]
    regularMarketPrice = ticker_info.info["regularMarketPrice"]

    # https://indepth-markets.com/matplotlib/get_ticker_info/
    trailingEps = ticker_info.info["trailingEps"] # 実質EPS
    forwardEps = ticker_info.info["forwardEps"] # 予想EPS
    trailingPE = ticker_info.info["trailingPE"] # 実質PER
    forwardPE = ticker_info.info["forwardPE"] # 予想PER
    pbr = ticker_info.info["priceToBook"]

    data.append({
      "ticker": stock["ticker"],
      "name": stock["name"],
      "segment": stock["segment"],
      "dividendRate": dividendRate,
      "dividendYield": dividendYield,
      "previousClose": previousClose,
      "regularMarketPrice": regularMarketPrice,
      "trailingEps": trailingEps,
      "forwardEps": forwardEps,
      "trailingPE": trailingPE,
      "forwardPE": forwardPE,
      "pbr": pbr
    })

today = datetime.date.today()
today_yyyymmdd = today.strftime('%Y%m%d')
db_dpath = f"./db/{today_yyyymmdd}"
os.makedirs(db_dpath, exist_ok=True)

stocks_fpath = os.path.join(db_dpath, f"stocks.json")
with open(stocks_fpath, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# dump latest files
latest_dpath = f"./db/latest"
os.makedirs(latest_dpath, exist_ok=True)

latest_stocks_fpath = os.path.join(latest_dpath, f"stocks.json")
with open(latest_stocks_fpath, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
