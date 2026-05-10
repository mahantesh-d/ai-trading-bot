from .logging_setup import logger

class PaperTrading:
    def __init__(self, instrument, quantity, risk_reward_ratio):
        self.instrument = instrument
        self.quantity = quantity
        self.risk_reward_ratio = risk_reward_ratio
        self.position = None
        self.entry_price = 0
        self.stoploss = 0
        self.target = 0
        self.pnl = 0

    def execute_trade(self, signal, price, stoploss):
        """Executes a trade in paper trading mode."""
        if self.position is None:
            if signal == "BUY":
                self.position = "LONG"
                self.entry_price = price
                self.stoploss = stoploss
                self.target = price + (price - stoploss) * self.risk_reward_ratio
                logger.info(f"Paper trade executed: BUY {self.quantity} {self.instrument} at {price}")
                return True
            elif signal == "SELL":
                self.position = "SHORT"
                self.entry_price = price
                self.stoploss = stoploss
                self.target = price - (stoploss - price) * self.risk_reward_ratio
                logger.info(f"Paper trade executed: SELL {self.quantity} {self.instrument} at {price}")
                return True
        return False

    def check_exit_conditions(self, current_price):
        """Checks if the exit conditions for the current position are met."""
        if self.position == "LONG":
            if current_price <= self.stoploss:
                self.pnl = (self.stoploss - self.entry_price) * self.quantity
                logger.info(f"Stoploss hit for LONG position. PnL: {self.pnl}")
                self.position = None
                return True
            elif current_price >= self.target:
                self.pnl = (self.target - self.entry_price) * self.quantity
                logger.info(f"Target hit for LONG position. PnL: {self.pnl}")
                self.position = None
                return True
        elif self.position == "SHORT":
            if current_price >= self.stoploss:
                self.pnl = (self.entry_price - self.stoploss) * self.quantity
                logger.info(f"Stoploss hit for SHORT position. PnL: {self.pnl}")
                self.position = None
                return True
            elif current_price <= self.target:
                self.pnl = (self.entry_price - self.target) * self.quantity
                logger.info(f"Target hit for SHORT position. PnL: {self.pnl}")
                self.position = None
                return True
        return False
