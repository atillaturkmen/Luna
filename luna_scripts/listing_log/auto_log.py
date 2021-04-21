import os, sys
import time
import dateparser
import calendar
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape
import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv


ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()
    last_announcement = scraper.get_announcement()
    listing_time = None
    save_folder = os.path.join(ROOT, "trades")
    symbols = None
    active_processes = []
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            symbols = scraper.get_symbols()
            if symbols:
                time_str = scraper.get_listing_date()
                listing_time = calendar.timegm(dateparser.parse(time_str).timetuple())
        if listing_time is not None and time.time() + 60 >= listing_time:
            for symbol in symbols:
                for quote in symbols[symbol]:
                    bot = subprocess.Popen(
                        shlex.split(f"python3 log_listing.py {symbol+quote} {save_folder} {ENV_PATH}"),
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    active_processes.append(bot)
            listing_time = None
            symbols = None
        last_announcement = current_announcement
        time.sleep(60)
        for p in active_processes:
            if p.poll() is None:
                del p