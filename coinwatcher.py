#!/usr/bin/env python3
import urllib.request
import json

portfolio = {
    'bitcoin': 1.35,
    'bitcoin-cash': 1.5,
    'bitcoin-gold': 1.5,
    'ethereum': 4.07,
    'ethereum-classic': 4.5,
    'litecoin': 1.12,
    'zcash': 0.72,
    'peercoin': 5.16,
}
url = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=0'

def float_nonny(val):
    return 0.0 if val is None else float(val)

def print_coin(coin_id):
    def colored(val):
        modifier = '0;37'
        if val < -9:
            modifier = '1;31'
        elif val < -3:
            modifier = '0;31'
        elif val > 9:
            modifier = '1;32'
        elif val > 3:
            modifier = '0;32'
        r = '{:6.2f}'.format(val)
        return CSI + modifier + ';40m' + r + CSI + '0m'

    fmt = '{:>5s} | {:8.2f} | {:8.2f} | {:14.2f} | {} | {} | {}'
    coin = coins[coin_id] 
    CSI='\x1B['
    print(fmt.format(coin['symbol'], coin['€'], coin['$'], coin['vol'],
                     colored(coin['change_1h']),
                     colored(coin['change_1d']),
                     colored(coin['change_7d'])))

req = urllib.request.Request(url)
r = urllib.request.urlopen(req).read()
payload = json.loads(r.decode('utf-8'))
coins = {}
for entry in payload:
    coin = {}
    coin['symbol'] = entry['symbol'] 
    coin['€'] = float_nonny(entry['price_eur'])
    coin['$'] = float_nonny(entry['price_usd'])
    coin['vol'] = float_nonny(entry['24h_volume_eur'])
    coin['change_1h'] = float_nonny(entry['percent_change_1h'])
    coin['change_1d'] = float_nonny(entry['percent_change_24h'])
    coin['change_7d'] = float_nonny(entry['percent_change_7d'])
    coins[entry['id']] = coin
top_coins = [coin['id'] for coin in payload][:20]
my_coins = [coin for coin in top_coins if coin in portfolio]
my_coins += [coin for coin in portfolio if not coin in my_coins]
other_coins = [coin for coin in top_coins if not coin in portfolio]
print(' coin |       rate in       |  traded volume |    change within last   ')
print('      |     €    |    $     |  last 24h in € |  hour  |   day  |  week ')
print('-----------------------------------------------------------------------')
print('                           coins I am holding                          ')
print('-----------------------------------------------------------------------')
for coin_id in my_coins:
    print_coin(coin_id)
print('-----------------------------------------------------------------------')
print('                  other coins with large market caps                   ')
print('-----------------------------------------------------------------------')
for coin_id in other_coins:
    print_coin(coin_id)
print()
total = 0
for coin_id in my_coins:
    total += portfolio[coin_id] * coins[coin_id]['€']
print('my total portfolio value: {:.2f} €'.format(total))
print()
for coin_id in my_coins:
    symbol = coins[coin_id]['symbol']
    holding = portfolio[coin_id]
    value = holding * coins[coin_id]['€']
    total += value
    print('{:4.2f} {} = {:8.2f} €'.format(holding, symbol, value))
