Pyfaast
======

This is a python client for the `faa.st <http://faa.st>`_ API.

Please see the example.py for more information on how to use.

#### Installation
```BASH
python setup.py install
```

### Usage

```PYTHON
from pyfaast import Faast

faastObj = Faast() ### Faast(TESTNET = TRUE)  for testnet

```

#### Get Supported Currencies

```PYTHON
faastObj.get_supported_currencies()
```

Response:

```JSON
[
...,
{'cmcID': 'ethereum',
 'decimals': 18,
 'deposit': True,
 'iconUrl': 'https://testapi.faa.st/api/v1/public/static/img/coins/icon_ETH.png',
 'infoUrl': 'https://ethereum.org',
 'name': 'Ethereum',
 'receive': True,
 'symbol': 'ETH',
 'walletUrl': 'https://faa.st'}
,...
]
# Number of supported tokens (pairs):     391 # Sep 13 2018
```

#### Get pair price

```PYTHON
faastObj.get_pair_price(pair = "BTC_ETH")
```

Response:
```JSON
{
    "pair": "BTC_ETH",
    "price": 0.03002374,
    "deposit_amount": 0,
    "minimum_deposit": 0.00017925
}

```

## Trading
#### Create a Swap
```PYTHON
swapObj = faastObj.create_a_swap(swap_pair = "BTC_ETH",
                      withdrawal_address = "0x08d62881d04f62a02ee80f45abf454f418c60e99",
                      refund_address = None,
                      deposit_amount = 0,
                      user_id = "",
                      affiliate_margin = 5,
                      affiliate_payment_address = "0x08d62881d04f62a02ee80f45abf454f418c60e99"
                    )
Only swap_pair and withdrawal_address are mandatory
```

Response:

```JSON
{'affiliate_margin': 5,
 'affiliate_payment_address': '1fs4Vz12WGBgPe6LmE2TDnGeuAjFhws6k',
 'created_at': '2018-09-13T08:27:19.865Z',
 'deposit_address': '2N44At9pemAX3mXwXV86fdXsPRaoKYt5jqS',
 'deposit_currency': 'BTC',
 'refund_address': '0x08d62881d04f62a02ee80f45abf454f418c60e99',
 'status': 'awaiting deposit',
 'swap_id': 'df53cda2-ac44-4ed9-9439-1b7586bb3879',
 'user_id': '',
 'withdrawal_address': '0x08d62881d04f62a02ee80f45abf454f418c60e99',
 'withdrawal_currency': 'ETH'}

```

## TODO:
- implement function for `QUERY SWAPS BY WITHDRAWAL_ADDRESS OR USER_ID`




Testing
-------
__TESTS NOT IMPLEMENTED YET__

install the needed test deps::

    $ pip install vcrpy nose coverage

Now we we can run the tests::

    $ nosetests pyfaast --with-coverage --cover-package pyfaast

