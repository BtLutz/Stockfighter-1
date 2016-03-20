import sys
sys.path.insert(0,'~/Stockfighter')

from Stockfighter.Api import StockFighterApi
import logging
from pdb import set_trace

api_key = 'af098a75a49ab1f6f358d7af06c089a97a875ffd'
log_level = logging.DEBUG
api = StockFighterApi(api_key, log_level)
print(api.heartbeat())

level_id = 'first_steps'
api.gm_start(level_id)

venue = 'IPMLEX'
my_account = 'SAK99148619'
target_stock = 'MMC'

current_shares = 0
shares_needed = 100000

previous_price = 0

while current_shares < shares_needed:

    stock_quote = api.stock_quote(venue, target_stock)
    last_ask = stock_quote['last']

    if last_ask == previous_price:
        quantity = 5000
        direction = 'sell'
        order_type = 'limit'
        price = last_ask - 2
        stock_order = api.stock_order(venue, my_account, target_stock, price, quantity, direction, order_type)

        shares_sold = stock_order['qty']
        current_shares = current_shares - shares_sold
    else:
        quantity = 5000
        direction = 'buy'
        order_type = 'limit'
        price = last_ask
        stock_order = api.stock_order(venue, my_account, target_stock, price, quantity, direction, order_type)
        shares_bought = stock_order['qty']
        current_shares = current_shares + shares_bought

    print("%s %s" % (stock_order, price))
    previous_price = last_ask
