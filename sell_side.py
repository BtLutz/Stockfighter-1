from Stockfighter.Api import StockFighterApi
import logging
from pdb import set_trace
import numpy

api_key = 'af098a75a49ab1f6f358d7af06c089a97a875ffd'
log_level = logging.DEBUG
api = StockFighterApi(api_key, log_level)
print(api.heartbeat())

level_id = 'first_steps'
api.gm_start(level_id)

venue = 'IPMLEX'
my_account = 'SAK99148619'
target_stock = 'MMC'

previous_orderbook = api.stock_orderbook(venue, target_stock)
# Get the current average spead on order book
while True:
    orderbook = api.stock_orderbook(venue, target_stock)
    try:
        previous_bid = previous_orderbook['bids'][0]['price']
        previous_qty = previous_orderbook['bids'][0]['qty']
        bid = orderbook['bids'][0]['price']
        qty = orderbook['bids'][0]['qty']

        bid_prices = [bid['price'] for bid in orderbook['bids']]
        ask_prices = [ask['price'] for ask in orderbook['asks']]

        average_bid = numpy.average(bid_prices)
        average_ask = numpy.average(ask_prices)

        bid_to_use = average_bid + numpy.std(average_bid)
        ask_to_use = average_ask - numpy.std(average_ask)

        print("bid: %s | ask: %s" % (bid_to_use, ask_to_use))



# Move one SD up on bid and one SD down on ask
