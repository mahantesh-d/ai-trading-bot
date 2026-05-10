import pandas as pd
import numpy as np
from .logging_setup import logger

def calculate_vwap(df):
    """Calculates the Volume Weighted Average Price (VWAP)."""
    df["TP"] = (df["high"] + df["low"] + df["close"]) / 3
    df["PV"] = df["TP"] * df["volume"]
    df["TotalPV"] = df["PV"].cumsum()
    df["TotalVolume"] = df["volume"].cumsum()
    df["VWAP"] = df["TotalPV"] / df["TotalVolume"]
    return df

def calculate_ema(df, period):
    """Calculates the Exponential Moving Average (EMA)."""
    return df["close"].ewm(span=period, adjust=False).mean()

def calculate_atr(df, period):
    """Calculates the Average True Range (ATR)."""
    df["H-L"] = df["high"] - df["low"]
    df["H-PC"] = np.abs(df["high"] - df["close"].shift(1))
    df["L-PC"] = np.abs(df["low"] - df["close"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    return df["TR"].rolling(period).mean()

class TradingStrategy:
    def __init__(self, instrument, atr_period, ema_short_period, ema_long_period):
        self.instrument = instrument
        self.atr_period = atr_period
        self.ema_short_period = ema_short_period
        self.ema_long_period = ema_long_period
        self.position = None  # "LONG", "SHORT", or None

    def generate_signal(self, df):
        """
        Generates a trading signal based on the VWAP and EMA 9/21 strategy.
        """
        logger.info(f"Generating signal for {self.instrument}")
        
        # Calculate indicators
        df = calculate_vwap(df)
        df["EMA_SHORT"] = calculate_ema(df, self.ema_short_period)
        df["EMA_LONG"] = calculate_ema(df, self.ema_long_period)
        df["ATR"] = calculate_atr(df, self.atr_period)

        latest_data = df.iloc[-1]
        
        # Entry conditions
        if self.position is None:
            # Long entry: EMA short crosses above EMA long, and price is above VWAP
            if (
                latest_data["EMA_SHORT"] > latest_data["EMA_LONG"]
                and latest_data["close"] > latest_data["VWAP"]
            ):
                logger.info(f"Long entry signal for {self.instrument}")
                self.position = "LONG"
                return {"signal": "BUY", "price": latest_data["close"], "stoploss": latest_data["close"] - latest_data["ATR"]}
            
            # Short entry: EMA short crosses below EMA long, and price is below VWAP
            elif (
                latest_data["EMA_SHORT"] < latest_data["EMA_LONG"]
                and latest_data["close"] < latest_data["VWAP"]
            ):
                logger.info(f"Short entry signal for {self.instrument}")
                self.position = "SHORT"
                return {"signal": "SELL", "price": latest_data["close"], "stoploss": latest_data["close"] + latest_data["ATR"]}
        
        return {"signal": "HOLD"}
