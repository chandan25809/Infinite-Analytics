from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import asyncio
from fastapi import APIRouter
import ssl
from websocket import create_connection
import threading


app = APIRouter()

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def binance_websocket_all_coins():
    socket_url = 'wss://stream.binance.com:9443/ws/!miniTicker@arr'
    ws = create_connection(socket_url, sslopt={"cert_reqs": ssl.CERT_NONE})

    while True:
        try:
            response = ws.recv()
            tickers = json.loads(response)
            print(tickers)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    ws.close()

# Start the WebSocket connection in a separate thread
websocket_thread = threading.Thread(target=binance_websocket_all_coins)
# websocket_thread.start()


coin_data = {
    "btcusd": {
        "closes": [],
        "highs": [],
        "lows": [],
        "last_price": 0.0,
    }
}


def binance_websocket(cc: str, interval: str):
    socket_url = f'wss://stream.binance.com:9443/ws/{cc.lower()}t@kline_{interval}'

    def on_message(_, message):
        json_message = json.loads(message)
        candle = json_message['k']
        is_candle_closed = candle['x']
        close = float(candle['c'])
        high = float(candle['h'])
        low = float(candle['l'])

        if is_candle_closed:
            coin_data[cc]['closes'].append(close)
            coin_data[cc]['highs'].append(high)
            coin_data[cc]['lows'].append(low)
            coin_data[cc]['last_price'] = close

            print(f"{cc.upper()} Closes:", coin_data[cc]['closes'])
            print(f"{cc.upper()} Highs:", coin_data[cc]['highs'])
            print(f"{cc.upper()} Lows:", coin_data[cc]['lows'])
            print(f"{cc.upper()} Last Price:", coin_data[cc]['last_price'])

    def on_close(_, __, ___):
        print("Connection Closed")

    ws = create_connection(socket_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    while True:
        try:
            response = ws.recv()
            on_message(None, response)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    ws.close()

# Start the WebSocket connection in a separate thread
websocket_thread = threading.Thread(target=binance_websocket, args=('btcusd', '1m'))
websocket_thread.start()


@app.get("/api/coin/{symbol}")
async def get_coin_details(symbol: str):
    if symbol.lower() not in coin_data:
        raise HTTPException(status_code=404, detail="Coin not found")

    cc_data = coin_data[symbol.lower()]

    # Calculate the trend based on the change percentage
    trend = 'up' if cc_data['last_price'] >= cc_data['closes'][-2] else 'down'

    coin_details = {
        "symbol": symbol,
        "last_price": cc_data['last_price'],
        "trend": trend,
    }

    return JSONResponse(content=coin_details)

@app.get("/api/coin/{symbol}/graphs")
async def get_coin_graphs(symbol: str):
    if symbol.lower() not in coin_data:
        raise HTTPException(status_code=404, detail="Coin not found")

    cc_data = coin_data[symbol.lower()]

    graphs_data = {"symbol": symbol, "graphs": {"closes": cc_data['closes'], "highs": cc_data['highs'], "lows": cc_data['lows']}}
    return JSONResponse(content=graphs_data)