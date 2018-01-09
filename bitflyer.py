#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from marketplace import MarketPlace

class BitFlyer(MarketPlace):
    def __init__(self, credentials):
        super().__init__("https://api.bitflyer.jp")

    def getRate(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/v1/getexecutions?pruduct_code={pair}&count=1".format(**locals()))
        return obj[0]["price"] if not raw_data else obj

    def getTicker(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/v1/ticker?product_code={pair}".format(**locals()))
        if raw_data:
            return obj
        ticker = { "last": obj["ltp"], "bid": obj["best_bid"], "ask": obj["best_bid"], "high": None, "low": None, "volume": obj["volume"] }
        return ticker

    def getTradesHistory(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/v1/getexecutions?pruduct_code={pair}".format(**locals()))
        if raw_data:
            return obj
        trades = []
        for trade in obj:
            trades.append({ "date": trade["exec_date"] + "Z", "price": trade["price"], "amount": trade["size"], "type": "ask" if trade["side"] == "SELL" else "bid" })
        return trades

    def getOrderBooks(self, pair="btc_jpy"):
        return super().get("/v1/getboard?pruduct_code={pair}".format(**locals()))

    def getExchangeOrdersRateByAmount(self, type, amount, pair="btc_jpy", raw_data=False):
        rate = self.getRate(pair)
        return { "rate": rate, "amount": amount, "price": amount * rate }

    def getExchangeOrdersRateByPrice(self, type, price, pair="btc_jpy", raw_data=False):
        rate = self.getRate(pair)
        return { "rate": rate, "amount": price / rate, "price": price }

    def getMarkets(self, raw_data=False):
        obj = super().get("/v1/getmarkets")
        if raw_data:
            return obj
        pairs = []
        for pair in obj:
            pairs.append(pair["product_code"])
        return pairs
