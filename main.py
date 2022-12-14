import pprint
import pandas as pd
import os
import datetime
import json
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
data = [] 
for idx, (ticker, detail) in enumerate(sd.items()):
    if "trailingAnnualDividendYield" not in detail:
        continue
    if "trailingPE" not in detail:
        continue
    if not type(detail["trailingAnnualDividendYield"]) is float or detail["trailingAnnualDividendYield"] < 0.03:
        continue
    # print(ticker)
    # pprint.pprint(detail)
    name = stock_names[idx]
    segment = stock_segments[idx]
    trailingAnnualDividendRate = detail["trailingAnnualDividendRate"]
    trailingAnnualDividendYield = detail["trailingAnnualDividendYield"]
    trailingPE = detail["trailingPE"]
    previousClose = detail["previousClose"]

    data.append({
      "ticker": ticker,
      "name": name,
      "segment": segment,
      "trailingAnnualDividendRate": trailingAnnualDividendRate,
      "trailingAnnualDividendYield": trailingAnnualDividendYield,
      "eps": previousClose/trailingPE,
      "per": trailingPE,
      "previousClose": previousClose,
    })

stocks_fpath = os.path.join(db_dpath, f"stocks.json")
with open(stocks_fpath, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# dump latest files
latest_dpath = f"./db/latest"
os.makedirs(latest_dpath, exist_ok=True)

latest_tickers_fpath = os.path.join(latest_dpath, f"tickers.json")
with open(latest_tickers_fpath, 'w', encoding="utf-8") as f:
    json.dump(sd, f, indent = 4, ensure_ascii=False)

latest_stocks_fpath = os.path.join(latest_dpath, f"stocks.json")
with open(latest_stocks_fpath, 'w', encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)