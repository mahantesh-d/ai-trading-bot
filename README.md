# AI Trading Bot

This is a Python-based intraday trading bot that uses the Zerodha Kite Connect API. It is designed to be simple, modular, and easy to extend.

## Features

- **Zerodha Kite Connect Integration:** Connects to your Zerodha account to fetch real-time data.
- **Paper Trading Mode:** Test your strategies without risking real money.
- **Single Trade Per Day:** The bot will execute only one trade per day and then stop.
- **Intraday Only:** All positions are closed before the market closes.
- **VWAP + EMA 9/21 Strategy:** A simple and effective intraday trading strategy.
- **ATR Stoploss:** Uses the Average True Range (ATR) to set a dynamic stoploss.
- **Risk Reward 1:2:** The target is set to twice the risk.
- **WhatsApp Alerts:** Get real-time alerts on your WhatsApp.
- **Logging:** Detailed logging of all activities.
- **Modular Architecture:** The code is organized into modules for easy maintenance and extension.

## Requirements

- Python 3.7+
- A Zerodha Kite Connect account
- A Twilio account for WhatsApp alerts

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-trading-bot.git
   cd ai-trading-bot
   ```

2. **Create a virtual environment and install the dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   - Rename `.env.example` to `.env`.
   - Open the `.env` file and add your Zerodha Kite Connect API key, API secret, and access token.
   - Add your Twilio Account SID, Auth Token, and WhatsApp numbers.

## Usage

To start the trading bot, run the following command:

```bash
python src/main.py
```

The bot will run continuously and execute trades based on the defined strategy.

## Disclaimer

This project is for educational purposes only. Trading in the stock market involves risk. The author is not responsible for any financial losses.
