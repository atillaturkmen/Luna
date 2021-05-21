import argparse
import json
import os
import sys
from datetime import datetime
import time

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.gate_io.GateWebSocketApp import GateWebSocketApp


def return_parser():
    parser = argparse.ArgumentParser(description="Log minute trades in gate.io")
    parser.add_argument("symbol", type=str, help="trades to log (ex:BTC_USDT)")
    parser.add_argument("dump_path", type=str, help="directory to dump trades")
    parser.add_argument("-d", "--duration", type=int, dest="duration", help="time in seconds")
    return parser


args = return_parser().parse_args(sys.argv[1:])
SYMBOL = args.symbol.upper()
DURATION = 300  # in seconds
if args.duration:
    DURATION = args.duration
TRADES = []
START_TIME = time.time()


def write_data():
    time_str = datetime.utcfromtimestamp(START_TIME).strftime('%Y-%m-%d_%H.%M.%S')
    path = os.path.join(args.dump_path, SYMBOL + '_' + time_str + ".json")
    with open(path, 'w') as file:
        json.dump(TRADES, file)


def on_message(ws, message):
    # type: (GateWebSocketApp, str) -> None
    # handle whatever message you received
    global START_TIME
    message = json.loads(message)
    if message["event"] == "subscribe":
        START = time.time()
    if message["event"] == "update":
        TRADES.append(message)
        if time.time() - START >= DURATION:
            write_data()
            sys.exit()


def on_open(ws):
    # type: (GateWebSocketApp) -> None
    # subscribe to channels interested
    ws.subscribe("spot.trades", [SYMBOL], False)


if __name__ == "__main__":
    app = GateWebSocketApp("YOUR_API_KEY",
                           "YOUR_API_SECRET",
                           on_open=on_open,
                           on_message=on_message)
    app.run_forever(ping_interval=1)