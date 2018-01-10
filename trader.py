class Trader:
    def __init__(self, marketplace, credentials, name):
        self.market = marketplace(credentials)
        self.balance = { "jpy": 0.0 }
        self.volume = { "btc": 0.0 }
        self.rate = { "btc": 0.0 }
        self.name = name

    def deposit(self, money, brand="jpy"):
        self.balance[brand] += money

    def getBalance(self):
        return self.balance["jpy"] + self.volume["btc"] * self.getRate(pair="btc_jpy")

    def buyMaxOfBalance(self, pair="btc_jpy"):
        p = pair.split("_")
        try:
            res = self.market.getExchangeOrdersRateByPrice(type="buy", price=self.balance[p[1]], pair=pair)
            self.balance[p[1]] = 0
            self.volume[p[0]] += res["amount"]
            self.rate["btc"] = res["rate"]
        except:
            pass

    def sellAll(self, pair="btc_jpy"):
        p = pair.split("_")
        try:
            res = self.market.getExchangeOrdersRateByAmount(type="sell", amount=self.volume[p[0]], pair=pair)
            self.balance[p[1]] += res["price"]
            self.volume[p[0]] = 0
            self.rate["btc"] = res["rate"]
        except:
            pass

    def getRate(self, pair="btc_jpy"):
        try:
            return self.market.getRate(pair)
        except:
            return -1

    def test(self):
        print(self.market.getTicker())
        print(self.market.getRate())
        print(self.market.getTradesHistory())
        print(self.market.getOrderBooks())
        print(self.market.getExchangeOrdersRateByAmount("sell", 1))
        print(self.market.getExchangeOrdersRateByPrice("buy", 10000))
        print(self.market.getMarkets())
