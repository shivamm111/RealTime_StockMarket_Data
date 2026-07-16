import pandas as pd

url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

df = pd.read_json(url)

stocks = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK"
]

result = df[
    (df["name"].isin(stocks))
    & (df["exch_seg"] == "NSE")
]

print(result[["token", "symbol", "name"]])