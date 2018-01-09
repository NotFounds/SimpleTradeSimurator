import time
from datetime import datetime

from trader import Trader
from coincheck import CoinCheck
from zaif import Zaif
from bitflyer import BitFlyer

def main():
    traders = []
    traders.append(Trader(CoinCheck, None, "CoinCheck: "))
    traders.append(Trader(Zaif,      None, "     Zaif: "))
    traders.append(Trader(BitFlyer,  None, " bitFlyer: "))

    for trademan in traders:
        trademan.deposit(brand="jpy", money=10000)
        trademan.buyMaxOfBalance(pair="btc_jpy")
        date = datetime.now().strftime("%m-%d %H:%M:%S")
        name = trademan.name
        print("{date}\t{name} BUY".format(**locals()))

    while True:
        date = datetime.now().strftime("%m-%d %H:%M:%S")
        for trademan in traders:
            rate = trademan.getRate("btc_jpy")
            if rate >= 2000000:
                trademan.buyMaxOfBalance(pair="btc_jpy")
                name = trademan.name
                ratio = (rate - trademan.rate["btc"]) * 100 / trademan.rate["btc"]
                print("{date}\t{name} BUY  {ratio: +f}%".format(**locals()))
            elif rate < 1800000:
                trademan.sellAll("btc_jpy")
                ratio = abs(rate - trademan.rate["btc"]) * 100 / trademan.rate["btc"]
                print("{date}\t{name} SELL {ratio: +f}%".format(**locals()))

        print(date, end="\t")
        for trademan in traders:
            print("{:3f}".format(trademan.getBalance()), end="  ")
        print("")
        time.sleep(10)

if __name__ == '__main__':
    main()