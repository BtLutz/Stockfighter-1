from Stockfighter.Api import StockFighterApi
import logging
from pdb import set_trace
from numpy import abs, std

api_key = 'af098a75a49ab1f6f358d7af06c089a97a875ffd'
log_level = logging.DEBUG
api = StockFighterApi(api_key, log_level)
print(api.heartbeat())

level_id = 'sell-side'
api.gm_start(level_id)


my_account = 'FSB27964069'
venue = 'AAPEX'
target_stock = 'CRE'

previous_orderbook = api.stock_orderbook(venue, target_stock)

current_spread = 0
danger_zone = 500
one_thousand = 1000
zero = 0

while True:
    #try:
    orderbook = api.stock_orderbook(venue, target_stock)

    previous_bid = previous_orderbook['bids'][0]['price']
    previous_qty = previous_orderbook['bids'][0]['qty']
    bid = orderbook['bids'][0]['price']
    qty = orderbook['bids'][0]['qty']

    if previous_bid != bid and previous_qty != qty:

        my_orders = api.account_stock_orders(venue, my_account, \
                                             target_stock)

        shorts = [order['qty'] for order in my_orders['orders'] \
                    if order['direction'] == 'sell']
        longs  = [order['qty'] for order in my_orders['orders'] \
                    if order['direction'] == 'buy']

        if numpy.abs(sum(longs) - sum(shorts)) > danger_zone:
            if sum(longs) - sum(shorts) q < zero:
                # sell
                api.stock_order(venue, my_account, target_stock, \
                bid_to_use, danger_zone, 'buy', 'market')
            elif longs - shorts > zero:
                # buy
                api.stock_order(veue, my_account, target_stock, \
                ask_to_use, danger_zone, 'sell', 'market')

        bid_prices = [bid['price'] for bid in orderbook['bids']]
        ask_prices = [ask['price'] for ask in orderbook['asks']]

        bid_qtys = [bid['qty'] for bid in orderbook['bids']]
        ask_qtys = [ask['qty'] for ask in orderbook['asks']]

        average_bid_price = numpy.average(bid_prices)
        average_ask_price = numpy.average(ask_prices)

        average_bid_qty = int(numpy.average(bid_qtys))
        average_ask_qty = int(numpy.average(ask_qtys))

        bid_to_use = int(average_bid_price + numpy.std(bid_prices))
        ask_to_use = int(average_ask_price - numpy.std(ask_prices))

        print("bid: %s | ask: %s" % (bid_to_use, ask_to_use))

        api.stock_order(venue, my_account, target_stock, bid_to_use, \
                        average_bid_qty, 'buy', 'limit')
        api.stock_order(venue, my_account, target_stock, ask_to_use, \
                        average_ask_qty, 'sell', 'immediate-or-cancel')

        previous_orderbook = orderbook
    #except:
    #    print("Bad orderbook")
        #pass

# Move one SD up on bid and one SD down on ask
