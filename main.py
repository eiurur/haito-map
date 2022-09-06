import pprint
import pandas as pd
import os
import datetime
import json
import yfinance as yf


read_file = pd.read_excel(r"tosho.xls")
read_file.to_csv(r"tosho.csv", index = None, header=False)

codes = pd.read_csv(r"tosho.csv", usecols=[1,2,3])
stock_tickers = [f"{row[1]}.T" for row in codes.itertuples()]
stock_names = [f"{row[2]}" for row in codes.itertuples()]
stock_segments = [f"{row[3]}" for row in codes.itertuples()]

# dump stocks
data = [] 
ticks = " ".join(stock_tickers)
tickers = yf.Tickers(ticks)
for idx, (ticker, detail) in enumerate(tickers.tickers.items()):
    if "lastDividendValue" not in detail.info or detail.info["lastDividendValue"] is None:
        continue
    
    name = stock_names[idx]
    segment = stock_segments[idx]
    dividendRate = detail.info["lastDividendValue"] / detail.info["regularMarketPrice"]
    dividendYield = detail.info["lastDividendValue"]
    previousClose = detail.info["previousClose"]
    regularMarketPrice = detail.info["regularMarketPrice"]

    data.append({
      "ticker": ticker,
      "name": name,
      "segment": segment,
      "dividendRate": dividendRate,
      "dividendYield": dividendYield,
      "previousClose": previousClose,
      "regularMarketPrice": regularMarketPrice,
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
