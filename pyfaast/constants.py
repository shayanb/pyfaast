from enum import Enum

API_BASE = 'https://api.faa.st'
TEST_BASE = 'https://testapi.faa.st'

CONTENT_BASE = 'https://api.faa.st/api/v1/public/static/img/' # IPFS?

USER_AGENT = 'Faast API - Version Python 0.0.10.10.1.0'

HEADERS = {
     "Content-Type": "application/json; charset=utf-8",
     "version": USER_AGENT,
     "Accept": "application/json"
}


DEBUG_VARIABLES = {
     "ETH_address" : "0x08d62881d04f62a02ee80f45abf454f418c60e99",
     "BTC_address" : "1fs4Vz12WGBgPe6LmE2TDnGeuAjFhws6k",
     "swap_pair" : "BTC_ETH"
}







