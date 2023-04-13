import json
from binance.client import Client

# API anahtarlarını yükle
with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)

# Binance API'siyle bağlantı kur
client = Client(api_keys['binance_api_key'], api_keys['binance_api_secret'])

# Coin ve strateji belirle
coin = 'ETHBTC'
strategy = 'ema'

# EMA stratejisi için parametreleri ayarla
if strategy == 'ema':
    interval = '1h'
    ema_short_period = 20
    ema_long_period = 50

# Sonsuz döngüde stratejiye göre alım-satım yap
while True:
    # Kullanılacak stratejinin son fiyatını hesapla
    if strategy == 'ema':
        klines = client.get_historical_klines(coin, interval, '1 day ago UTC')
        close_prices = [float(kline[4]) for kline in klines]
        ema_short = sum(close_prices[-ema_short_period:]) / ema_short_period
        ema_long = sum(close_prices[-ema_long_period:]) / ema_long_period
        last_price = float(client.get_symbol_ticker(symbol=coin)['price'])
        if last_price > ema_long and last_price > ema_short:
            # Alım yap
            quantity = 0.1 # Örnek miktar, kendinize göre ayarlayın
            buy_price = 0.05000000 # Almak istediğiniz fiyat
            buy_order = client.create_order(
                symbol=coin,
                side='BUY',
                type='LIMIT',
                timeInForce='GTC', # Kalıcı olarak beklet
                price=buy_price,
                quantity=quantity
            )
            print(f'Bought {quantity} {coin} at {buy_price}')
        elif last_price < ema_long and last_price < ema_short:
            # Satım yap
            sell_price = 0.05500000 # Satmak istediğiniz fiyat
            sell_order = client.create_order(
                symbol=coin,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC', # Kalıcı olarak beklet
                price=sell_price,
                quantity=quantity
            )
            print(f'Sold {quantity} {coin} at {sell_price}')
    
    # Belirli bir süre
