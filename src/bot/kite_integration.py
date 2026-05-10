from kiteconnect import KiteConnect
from .logging_setup import logger
import pandas as pd

class KiteIntegration:
    def __init__(self, api_key, access_token):
        self.kite = KiteConnect(api_key=api_key)
        try:
            self.kite.set_access_token(access_token)
            logger.info("Kite Connect session created successfully.")
        except Exception as e:
            logger.error(f"Error creating Kite Connect session: {e}")
            raise

    def get_historical_data(self, instrument_token, from_date, to_date, interval):
        """Fetches historical data for a given instrument."""
        try:
            records = self.kite.historical_data(instrument_token, from_date, to_date, interval)
            df = pd.DataFrame(records)
            df["date"] = pd.to_datetime(df["date"])
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    def get_instrument_token(self, instrument_name, exchange="NSE"):
        """Retrieves the instrument token for a given instrument name."""
        try:
            instruments = self.kite.instruments(exchange)
            for instrument in instruments:
                if instrument["tradingsymbol"] == instrument_name:
                    return instrument["instrument_token"]
            logger.warning(f"Instrument token not found for {instrument_name}")
            return None
        except Exception as e:
            logger.error(f"Error fetching instrument token: {e}")
            return None
