#!/usr/bin/python
# -*- coding: utf-8 -*-
from wicc.cryptos.coins.base import BaseCoin


class WaykiCoin(BaseCoin):
    coin_symbol = "WICC"
    display_name = "WaykiChain"
    enabled = True
    magicbyte = 73
    segwit_supported = True
    # script_magicbyte = 51
    script_magicbyte = 0x1a1d42ff
    hd_path = 99999
    wif_prefix = 153
    testnet_overrides = {
        'display_name': "WaykiChain Testnet",
        'coin_symbol': "wicc",
        'wif_prefix': 210,
        "hd_path": 99999,
        'magicbyte': 135,
        'script_magicbyte': 0xd75c7dfd
    }
