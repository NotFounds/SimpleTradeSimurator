#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from marketplace import MarketPlace

class CoinCheck(MarketPlace):
    def __init__(self, credentials):
        super().__init__("https://coincheck.com")

    def getRate(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/rate/{pair}".format(**locals()))
        return float(obj["rate"]) if not raw_data else obj

    def getTicker(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/ticker")
        if raw_data:
            return obj
        ticker = { "last": obj["last"], "bid": obj["bid"], "ask": obj["bid"], "high": obj["high"], "low": obj["low"], "volume": obj["volume"] }
        return ticker

    def getTradesHistory(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/trades?pair={pair}".format(**locals()))
        if raw_data:
            return obj
        trades = []
        for trade in obj["data"]:
            trades.append({ "date": trade["created_at"], "price": trade["rate"], "amount": float(trade["amount"]), "type": "ask" if trade["order_type"] == "sell" else "bid" })
        return trades

    def getOrderBooks(self, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/order_books")
        if raw_data:
            return obj
        mid = (float(obj["asks"][0][0]) + float(obj["bids"][0][0])) / 2
        asks = []
        for ask in obj["asks"]:
            asks.append({ "price": float(ask[0]), "size": float(ask[1]) })
        bids = []
        for bid in obj["bids"]:
            bids.append({ "price": float(bid[0]), "size": float(bid[1]) })
        return { "mid_price": mid, "asks": asks, "bids": bids }

    def getExchangeOrdersRateByAmount(self, type, amount, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/exchange/orders/rate?order_type={type}&amount={amount}&pair={pair}".format(**locals()))
        return { "rate": float(obj["rate"]), "amount": float(obj["amount"]), "price": float(obj["rate"]) } if not raw_data else obj

    def getExchangeOrdersRateByPrice(self, type, price, pair="btc_jpy", raw_data=False):
        obj = super().get("/api/exchange/orders/rate?order_type={type}&price={price}&pair={pair}".format(**locals()))
        return { "rate": float(obj["rate"]), "amount": float(obj["amount"]), "price": float(obj["price"]) } if not raw_data else obj

    def getMarkets(self):
        return ["btc_jpy"]