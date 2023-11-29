import yfinance as yf
import tkinter as tk
import time
import threading
import os
import configparser

CONFIG_FILE = os.path.expanduser('~/.config/pyahoo')

def load_config():
    config = configparser.ConfigParser()
    symbols = {
        'BTC-USD': 'Bitcoin',
        'DOGE-USD': 'Dogecoin',
        'AAPL': 'Apple',
        'TSLA': 'Tesla'
    }
    sleep_time = 300  # 5 minutes by default
    font_size = 12  # Default font size

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'Settings' in config:
            symbols_str = config['Settings'].get('symbols')
            sleep_time = config['Settings'].getint('sleep_time')
            font_size = config['Settings'].getint('font_size')

            try:
                symbols = eval(symbols_str)
                if not isinstance(symbols, dict):
                    symbols = {}
            except Exception as e:
                print(f"Error reading symbols from config: {e}")
                symbols = {}

    return symbols, sleep_time, font_size

def update_prices(symbols, sleep_time, font_size):
    while True:
        prices_text = "\n===== Current Prices =====\n"
        for symbol, name in symbols.items():
                tickers = yf.Ticker(symbol)
                price = tickers.history(period='1mo')['Close'].iloc[-1]
                prices_text += f'{name}: ${price:.6f}\n'

        label.config(text=prices_text, font=('Arial', font_size))
        time.sleep(sleep_time)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stock and Crypto Prices")

    label = tk.Label(root, justify='left', padx=10, pady=10)
    label.pack()

    symbols, sleep_time, font_size = load_config()

    update_thread = threading.Thread(target=update_prices, args=(symbols, sleep_time, font_size))
    update_thread.daemon = True
    update_thread.start()

    root.mainloop()

    # Save settings to config file when the program exits
    config = configparser.ConfigParser()
    config['Settings'] = {
        'symbols': str(symbols),
        'sleep_time': str(sleep_time),
        'font_size': str(font_size)
    }

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

