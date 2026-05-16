import pandas as pd
import numpy as np

from .logging_setup import logger


def calculate_vwap(df):
    df["tp"] = (
        df["high"] +
        df["low"] +
        df["close"]
    ) / 3

    df["pv"] = df["tp"] * df["volume"]

    df["total_pv"] = df["pv"].cumsum()

    df["total_volume"] = df["volume"].cumsum()

    df["vwap"] = (
        df["total_pv"] /
        df["total_volume"]
    )

    return df


def calculate_ema(df, period):
    return df["close"].ewm(
        span=period,
        adjust=False
    ).mean()


def calculate_atr(df, period):
    df["h-l"] = df["high"] - df["low"]

    df["h-pc"] = abs(
        df["high"] -
        df["close"].shift(1)
    )

    df["l-pc"] = abs(
        df["low"] -
        df["close"].shift(1)
    )

    df["tr"] = df[
        ["h-l", "h-pc", "l-pc"]
    ].max(axis=1)

    return df["tr"].rolling(period).mean()


class TradingStrategy:
    def __init__(
        self,
        instrument,
        atr_period,
        ema_short_period,
        ema_long_period
    ):
        self.instrument = instrument

        self.atr_period = atr_period

        self.ema_short_period = ema_short_period

        self.ema_long_period = ema_long_period

        self.position = None

    def generate_signal(self, df):
        try:
            logger.info(
                f"Generating signal for {self.instrument}"
            )

            # Indicators
            df = calculate_vwap(df)

            df["ema_short"] = calculate_ema(
                df,
                self.ema_short_period
            )

            df["ema_long"] = calculate_ema(
                df,
                self.ema_long_period
            )

            df["atr"] = calculate_atr(
                df,
                self.atr_period
            )

            latest = df.iloc[-1]

            # BUY SIGNAL
            if (
                latest["ema_short"] >
                latest["ema_long"]
                and
                latest["close"] >
                latest["vwap"]
            ):
                logger.info("BUY signal generated")

                return {
                    "signal": "BUY",
                    "price": latest["close"],
                    "stoploss": (
                        latest["close"] -
                        latest["atr"]
                    )
                }

            # SELL SIGNAL
            elif (
                latest["ema_short"] <
                latest["ema_long"]
                and
                latest["close"] <
                latest["vwap"]
            ):
                logger.info("SELL signal generated")

                return {
                    "signal": "SELL",
                    "price": latest["close"],
                    "stoploss": (
                        latest["close"] +
                        latest["atr"]
                    )
                }

            logger.info("No trade signal generated")

            return {
                "signal": "HOLD"
            }

        except Exception as e:
            logger.error(f"Strategy error: {e}")

            return {
                "signal": "HOLD"
            }