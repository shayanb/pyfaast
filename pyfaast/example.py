import sys
from pprint import pprint
sys.path.append('../')

from pyfaast import Faast


faastObj = Faast(TESTNET = True) #kwargs

btc_eth = faastObj.get_pair_price(pair = "BTC_ETH")

print (btc_eth)

supported_currencies = faastObj.get_supported_currencies()

for currency in supported_currencies:
	print (currency.get("symbol", None))
print("Number of supported tokens (pairs):\t%s" % len(supported_currencies))
pprint(supported_currencies[1])

swapObj = faastObj.create_a_swap(debug=True)

pprint (swapObj)


#pprint (faastObj.fetch_swap(swap_id=swapObj.get("swap_id"), debug = True))






