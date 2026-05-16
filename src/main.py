import time
import json
import yfinance as yf

from bot import config
from bot.logging_setup import logger
from bot.strategy import TradingStrategy
from bot.paper_trading import PaperTrading


def update_state(state):
    with open("src/state.json", "w") as f:
        json.dump(state, f)


def fetch_market_data():
    try:
        ticker = yf.Ticker("RELIANCE.NS")

        df = ticker.history(
            period="5d",
            interval="5m"
        )

        if df.empty:
            logger.warning("No market data received.")
            return None

        # Convert columns to lowercase
        df.columns = [col.lower() for col in df.columns]

        logger.info("Market data fetched successfully.")
        return df
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return None


def main():
    logger.info("Starting trading bot...")

    # Initial state
    state = {
        "bot_status": "RUNNING",
        "signal": "NONE",
        "position": "NONE",
        "daily_pnl": 0
    }

    update_state(state)

    # Strategy
    strategy = TradingStrategy(
        instrument=config.INSTRUMENT,
        atr_period=config.ATR_PERIOD,
        ema_short_period=config.EMA_SHORT_PERIOD,
        ema_long_period=config.EMA_LONG_PERIOD,
    )

    # Paper Trading
    paper_trader = PaperTrading(
        instrument=config.INSTRUMENT,
        quantity=config.QUANTITY,
        risk_reward_ratio=config.RISK_REWARD_RATIO,
    )

    while True:
        try:
            # Fetch market data
            df = fetch_market_data()

            if df is None:
                time.sleep(60)
                continue

            # Generate signal
            signal_data = strategy.generate_signal(df)

            logger.info(
                f"Generated Signal: {signal_data}"
            )

            # Update dashboard state
            state["signal"] = signal_data.get(
                "signal",
                "NONE"
            )

            state["position"] = (
                paper_trader.position
                if paper_trader.position
                else "NONE"
            )

            state["daily_pnl"] = paper_trader.pnl

            update_state(state)

            # Execute paper trade
            if paper_trader.position is None:
                if signal_data["signal"] in [
                    "BUY",
                    "SELL"
                ]:
                    trade_executed = (
                        paper_trader.execute_trade(
                            signal=signal_data["signal"],
                            price=signal_data["price"],
                            stoploss=signal_data["stoploss"]
                        )
                    )

                    if trade_executed:
                        logger.info(
                            "Paper trade executed."
                        )
                        state["position"] = (
                            paper_trader.position
                        )
                        update_state(state)
            else:
                current_price = df.iloc[-1]["close"]

                if paper_trader.check_exit_conditions(
                    current_price
                ):
                    logger.info(
                        f"Trade closed. "
                        f"PnL: {paper_trader.pnl}"
                    )

                    state["daily_pnl"] = (
                        paper_trader.pnl
                    )

                    state["position"] = "NONE"

                    update_state(state)

            logger.info(
                "Waiting for next candle..."
            )

            time.sleep(300)
        except Exception as e:
            logger.error(
                f"Main loop error: {e}"
            )
            time.sleep(60)


if __name__ == "__main__":
    main()