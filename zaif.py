#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from marketplace import MarketPlace

class Zaif(MarketPlace):
    def __init__(self, credentials):
        super().__init__("https://api.zaif.jp/api/1")

    def getRate(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/last_price/{pair}".format(**locals()))
        return obj["last_price"] if not raw_data else obj

    def getTicker(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/ticker/{pair}".format(**locals()))
        if raw_data:
            return obj
        ticker = { "last": obj["last"], "bid": obj["bid"], "ask": obj["bid"], "high": obj["high"], "low": obj["low"], "volume": obj["volume"] }
        return ticker

    def getTradesHistory(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/trades/{pair}".format(**locals()))
        if raw_data:
            return obj
        trades = []
        for trade in obj:
            date = datetime.datetime.fromtimestamp(trade["date"], tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            trades.append({ "date": date, "price": trade["price"], "amount": trade["amount"], "type": trade["trade_type"] })
        return trades

    def getOrderBooks(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/depth/{pair}".format(**locals()))
        if raw_data:
            return obj
        mid = (obj["asks"][0][0] + obj["bids"][0][0]) / 2
        asks = []
        for ask in obj["asks"]:
            asks.append({ "price": ask[0], "size": ask[1] })
        bids = []
        for bid in obj["bids"]:
            bids.append({ "price": bid[0], "size": bid[1] })
        return { "mid_price": mid, "asks": asks, "bids": bids }

    def getExchangeOrdersRateByAmount(self, type, amount, pair="btc_jpy", raw_data=False):
        rate = self.getRate(pair)
        return { "rate": rate, "amount": amount, "price": amount * rate }

    def getExchangeOrdersRateByPrice(self, type, price, pair="btc_jpy", raw_data=False):
        rate = self.getRate(pair)
        return { "rate": rate, "amount": price / rate, "price": price }

    def getMarkets(self, raw_data=False):
        obj = super().get("/currency_pairs/all")
        if raw_data:
            return obj
        pairs = []
        for pair in obj:
            pairs.append(pair["currency_pair"])
        return pairs
