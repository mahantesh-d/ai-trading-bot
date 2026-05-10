import time
from datetime import datetime, timedelta
from bot import config
from bot.logging_setup import logger
from bot.strategy import TradingStrategy
from bot.paper_trading import PaperTrading
from bot.kite_integration import KiteIntegration
from bot.kite_auth import KiteAuth
from bot.notifications import WhatsAppNotifier

def main():
    """Main function to run the trading bot."""
    logger.info("Starting the trading bot...")

    # Initialize components
    try:
        auth = KiteAuth(api_key=config.KITE_API_KEY, api_secret=config.KITE_API_SECRET)
        access_token = auth.get_access_token()

        kite = KiteIntegration(
            api_key=config.KITE_API_KEY,
            access_token=access_token,
        )
        strategy = TradingStrategy(
            instrument=config.INSTRUMENT,
            atr_period=config.ATR_PERIOD,
            ema_short_period=config.EMA_SHORT_PERIOD,
            ema_long_period=config.EMA_LONG_PERIOD,
        )
        paper_trader = PaperTrading(
            instrument=config.INSTRUMENT,
            quantity=config.QUANTITY,
            risk_reward_ratio=config.RISK_REWARD_RATIO,
        )
        notifier = WhatsAppNotifier()
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return

    instrument_name = config.INSTRUMENT.split(":")[1]
    instrument_token = kite.get_instrument_token(instrument_name)
    if not instrument_token:
        logger.error(f"Could not find instrument token for {instrument_name}")
        return

    # Main loop
    while True:
        try:
            # Fetch historical data
            to_date = datetime.now()
            from_date = to_date - timedelta(days=30)  # Fetch last 30 days of data
            df = kite.get_historical_data(
                instrument_token, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"), "5minute"
            )

            if not df.empty:
                # Generate signal
                signal_data = strategy.generate_signal(df)

                # Execute trade
                if paper_trader.position is None:
                    if signal_data["signal"] in ["BUY", "SELL"]:
                        if paper_trader.execute_trade(signal_data["signal"], signal_data["price"], signal_data["stoploss"]):
                            notifier.send_message(
                                f"Trade executed: {signal_data['signal']} {config.QUANTITY} {config.INSTRUMENT} at {signal_data['price']}"
                            )
                else:
                    # Check for exit
                    if paper_trader.check_exit_conditions(df.iloc[-1]["close"]):
                        notifier.send_message(
                            f"Trade closed for {config.INSTRUMENT}. PnL: {paper_trader.pnl}"
                        )
                        break  # Exit after one trade per day

            time.sleep(300)  # Wait for 5 minutes
        except Exception as e:
            logger.error(f"An error occurred in the main loop: {e}")
            time.sleep(300)

if __name__ == "__main__":
    main()
