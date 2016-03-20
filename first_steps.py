from Stockfighter.Api import StockFighterApi
import logging
from pdb import set_trace

api_key = 'af098a75a49ab1f6f358d7af06c089a97a875ffd'
log_level = logging.DEBUG
api = StockFighterApi(api_key, log_level)
print(api.heartbeat())

level_id = 'first_steps'
api.gm_start(level_id)

venue = 'ZNYEX'
my_account = 'BAH10537086'
target_stock = 'FMH'

current_shares = 0
shares_needed = 100

while current_shares < shares_needed:

    stock_quote = api.stock_quote(venue, target_stock)
    last_ask = stock_quote['last']

    quantity = 5
    direction = 'buy'
    order_type = 'limit'
    stock_order = api.stock_order(venue, my_account, target_stock, last_ask, quantity, direction, order_type)

    print(stock_order)
    current_shares = current_shares + 5
