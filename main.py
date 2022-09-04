import pprint
import pandas as pd
import datetime
import yfinance as yf


read_file = pd.read_excel(r"data_j.xls")
read_file.to_csv(r"data_j.csv", index = None, header=False)
codes = pd.read_csv(r"data_j.csv", usecols=[1,2])
stock_tickers = [f"{row[1]}.T" for row in codes.itertuples()]
stock_names = [f"{row[2]}.T" for row in codes.itertuples()]


today = datetime.date.today()
start = datetime.datetime.now() - datetime.timedelta(days=7)
end = today

# stocks.append("^N225")
tickers = yf.Tickers(" ".join(stock_tickers))

closes   = [] # 終値

for idx, ticker in enumerate(tickers.tickers):
    cursor = tickers.tickers[ticker]
    name = stock_names[idx]
    dividendRate = cursor.info["dividendRate"]
    dividendYield = cursor.info["dividendYield"]
    print(ticker, name, dividendYield, cursor.history(period="1wk").Close.tail())
    closes.append({
      "ticker": ticker,
      "name": name,
      "dividendRate": dividendRate,
      "dividendYield": dividendYield,
      "close": cursor.history(period="1wk").Close.tail(),
    })

closes = pd.DataFrame(closes).T   # DataFrame化
closes.columns = stocks           # カラム名の設定
closes = closes.ffill()           # 欠損データの補完
print(closes)


today_yyyymmdd = today.strftime('%Y%m%d')
fname = f"stock_{today_yyyymmdd}.json"
with open(fname, 'w') as f:
    json.dump(d, f, indent=4)

# 会社概要(info)を出力
# pprint.pprint(ticker_info.info)
