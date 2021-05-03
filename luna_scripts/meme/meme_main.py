import argparse
import os
import random
import sys
import time
from binance.client import Client
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper

DATABASE_PATH = os.path.join(ROOT, "luna_scripts", "listing_mail", "mailing_list.db")
ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])


emailWrapper = EmailWrapper(
        port=os.environ["ssl_port"],
        smtp_server=os.environ["smtp_server"],
        sender_email=os.environ["email"],
        password=os.environ["email_password"]
)


def send_bogdanoff(ticker):
    subject = "Dump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "dump/" + random.choice(os.listdir(os.path.join(ROOT, "luna_scripts", "meme", "dump")))
    emailWrapper.database_send(subject, body, img)


def send_jesse(ticker):
    subject = "Pump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "pump/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "pump"))))
    emailWrapper.database_send(subject, body, img)


def get_vitalik_on_the_line(ticker):
    subject = "Get Vitalik On The Line --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "vitalik/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "vitalik"))))
    emailWrapper.database_send(subject, body, img)


def return_parser():
    parser = argparse.ArgumentParser(description="Send pump dump memes via email")
    parser.add_argument("ticker", type=str, help="Ticker to watch")
    return parser


if __name__ == '__main__':
    args = return_parser().parse_args(sys.argv[1:])
    TICKER = args.ticker.upper()
    initial_price = float(client.get_symbol_ticker(symbol=TICKER)["price"])
    i = 0
    while True:
        price = float(client.get_symbol_ticker(symbol=TICKER)["price"])
        if price < initial_price * 0.9:
            send_bogdanoff(TICKER)
            initial_price = price
        if price > initial_price * 1.5:
            get_vitalik_on_the_line(TICKER)
            initial_price = price
        elif price > initial_price * 1.1:
            send_jesse(TICKER)
            initial_price = price
        # update old price every hour
        i += 1
        if i % 60 == 0:
            initial_price = price
        time.sleep(60)
