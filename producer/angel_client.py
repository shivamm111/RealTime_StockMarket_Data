from SmartApi import SmartConnect
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
MPIN = os.getenv("ANGEL_MPIN")


def login():

    smart_api = SmartConnect(api_key=API_KEY)

    otp = input("Enter current OTP from Authenticator: ")

    session = smart_api.generateSession(
        CLIENT_CODE,
        MPIN,
        otp
    )

    return {
        "jwt_token": session["data"]["jwtToken"],
        "feed_token": session["data"]["feedToken"],
        "client_code": CLIENT_CODE,
        "api_key": API_KEY
    }