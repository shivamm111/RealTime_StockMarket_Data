from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from angel_client import login
from kafka_producer import send_tick
from datetime import datetime, timezone

# --------------------------------
# LOGIN
# --------------------------------

session = login()

AUTH_TOKEN = session["jwt_token"]
API_KEY = session["api_key"]
CLIENT_CODE = session["client_code"]
FEED_TOKEN = session["feed_token"]

# --------------------------------
# TOKEN MAPPING
# --------------------------------

TOKEN_MAP = {
    "2885": "RELIANCE",
    "11536": "TCS",
    "1594": "INFY",
    "1333": "HDFCBANK",
    "4963": "ICICIBANK"
}

# --------------------------------
# WEBSOCKET
# --------------------------------

sws = SmartWebSocketV2(
    AUTH_TOKEN,
    API_KEY,
    CLIENT_CODE,
    FEED_TOKEN
)


# --------------------------------
# CALLBACKS
# --------------------------------

def on_open(wsapp):
    print("✅ WebSocket Connected")

    token_list = [
        {
            "exchangeType": 1,
            "tokens": [
                "2885",   # RELIANCE
                "11536",  # TCS
                "1594",   # INFY
                "1333",   # HDFCBANK
                "4963"    # ICICIBANK
            ]
        }
    ]

    sws.subscribe(
        correlation_id="marketfeed",
        mode=1,  # LTP Mode
        token_list=token_list
    )

    print("✅ Subscribed to 5 Stocks")


def on_data(wsapp, message):

    token = message.get("token")

    symbol = TOKEN_MAP.get(token, token)

    ltp = message.get("last_traded_price", 0) / 100

    exchange_time = message.get("exchange_timestamp")

    tick = {
        "symbol": symbol,
        "token": token,
        "price": ltp,
        "exchange_timestamp": exchange_time,
        "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        "exchange": "NSE"
}

    send_tick(tick)

    print(
        f"{symbol:<12} | ₹{ltp:<10}"
    )


def on_error(wsapp, error):
    print("\n❌ ERROR")
    print(error)


def on_close(wsapp):
    print("\n🔴 CONNECTION CLOSED")


# --------------------------------
# ATTACH CALLBACKS
# --------------------------------

sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

# --------------------------------
# START
# --------------------------------

print("🚀 Connecting to Angel One...")

sws.connect()