import os
from dotenv import load_dotenv

load_dotenv()

# Kite Connect API credentials
KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_API_SECRET = os.getenv("KITE_API_SECRET")

# WhatsApp (Twilio) credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

# Trading parameters
INSTRUMENT = os.getenv("INSTRUMENT", "NSE:RELIANCE")
QUANTITY = int(os.getenv("QUANTITY", 1))
RISK_REWARD_RATIO = float(os.getenv("RISK_REWARD_RATIO", 2))
ATR_PERIOD = int(os.getenv("ATR_PERIOD", 14))
EMA_SHORT_PERIOD = int(os.getenv("EMA_SHORT_PERIOD", 9))
EMA_LONG_PERIOD = int(os.getenv("EMA_LONG_PERIOD", 21))
