from Stockfighter.Api import StockFighterApi
import logging
from pdb import set_trace
from numpy import average, std
import time

class order:
    __init__(self, venue, stock, bid, ask, direction, quantity, filled):
        self.venue = venue
        self.stock = stock
        self.bid = bid
        self.ask = ask
        self.direction = direction
        self.quantity = quantity
        self.filled = filled


api_key = 'af098a75a49ab1f6f358d7af06c089a97a875ffd'
log_level = logging.DEBUG
api = StockFighterApi(api_key, log_level)
print(api.heartbeat())

level_id = 'sell-side'
api.gm_start(level_id)


my_account = 'AAM312666'
venue = 'MMTEX'
target_stock = 'TBI'

previous_orderbook = api.stock_orderbook(venue, target_stock)

current_spread = 0
danger_zone = 500
one_thousand = 1000
zero = 0

orders = []

while True:
        orderbook = api.stock_orderbook(venue, target_stock)
        if orderbook['bids'] and orderbook['asks']:

            bid_prices = [bid['price'] for bid in orderbook['bids']]
            ask_prices = [ask['price'] for ask in orderbook['asks']]

            bid_qtys = [bid['qty'] for bid in orderbook['bids']]
            ask_qtys = [ask['qty'] for ask in orderbook['asks']]

            average_bid_price = average(bid_prices)
            average_ask_price = average(ask_prices)

            average_bid_qty = int(average(bid_qtys))
            average_ask_qty = int(average(ask_qtys))

            bid_to_use = int(average_bid_price + std(bid_prices))
            ask_to_use = int(average_ask_price - std(ask_prices))


            print("bid: %s | ask: %s" % (bid_to_use, ask_to_use))

            for order in orders:
                if average_ask >= order.ask and direction == 'buy':
                    api.stock_order(venue, my_account, target_stock, \
                    order.ask, order.quantity, 'sell', 'limit')
                elif average_bid >= order.bid and direction == 'sell':
                    api.stock_order(venue, my_account, target_stock, \
                    order.bid, order.quantity, 'buy', 'limit')

            api.stock_order(venue, my_account, target_stock, bid_to_use, \
                            int(average_bid_qty / 10), 'buy', 'limit')
            time.sleep(1)
            api.stock_order(venue, my_account, target_stock, ask_to_use, \
                            int(average_ask_qty / 10), 'sell', 'immediate-or-cancel')
            time.sleep(1)
            my_orders = api.account_stock_orders(venue, my_account, \
                                                 target_stock)

            shorts = [order['qty'] for order in my_orders['orders'] \
                        if order['direction'] == 'sell']
            longs  = [order['qty'] for order in my_orders['orders'] \
                        if order['direction'] == 'buy']

            if abs(sum(longs) - sum(shorts)) > danger_zone:
                print(sum(longs) - sum(shorts))
                if sum(longs) - sum(shorts) > zero:
                    # sell
                    api.stock_order(venue, my_account, target_stock, \
                    bid_to_use, danger_zone, 'sell', 'market')
                    time.sleep(1)
                elif sum(longs) - sum(shorts) < zero:
                    # buy
                    api.stock_order(venue, my_account, target_stock, \
                    ask_to_use, danger_zone, 'buy', 'market')
                    time.sleep(1)
            previous_orderbook = orderbook
