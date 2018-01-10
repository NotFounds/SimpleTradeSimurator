import time
from datetime import datetime
from colorama import init, Fore

from trader import Trader
from coincheck import CoinCheck
from zaif import Zaif
from bitflyer import BitFlyer

init()

One_Satoshi = 0.00000001
Capital = 10000

def main():
    traders = []
    traders.append(Trader(CoinCheck, None, "CoinCheck: "))
    traders.append(Trader(Zaif,      None, "     Zaif: "))
    traders.append(Trader(BitFlyer,  None, " bitFlyer: "))

    first_rate = {}
    last_rate = {}
    last_balance = {}
    for trademan in traders:
        trademan.deposit(brand="jpy", money=Capital)
        trademan.buyMaxOfBalance(pair="btc_jpy")
        date = datetime.now().strftime("%m-%d %H:%M:%S")
        name = trademan.name
        rate = trademan.getRate("btc_jpy")
        amount = trademan.volume["btc"]
        first_rate[name] = rate
        last_rate[name] = rate
        last_balance[name] = trademan.getBalance()
        print("{date}\t{name} BUY  {rate}  {amount}".format(**locals()))

    while True:
        date = datetime.now().strftime("%m-%d %H:%M:%S")
        for trademan in traders:
            rate = trademan.getRate("btc_jpy")
            last = trademan.rate["btc"]
            name = trademan.name
            ratio = (rate - trademan.rate["btc"]) * 100 / trademan.rate["btc"]
            if rate < last: # 売ったときより安くなれば買う
                if trademan.balance["jpy"] > rate * One_Satoshi: # 予算の有無
                    trademan.buyMaxOfBalance(pair="btc_jpy")
                    amount = trademan.volume["btc"]
                    print("{date}\t{name} BUY  {rate}  {amount}".format(**locals()))
            elif rate >= last and ratio > 0.05: # 利益が0.05%以上になったら売る
                if trademan.volume["btc"] > One_Satoshi: # 売るものがあるか確認
                    benefit = (rate - trademan.rate["btc"]) * trademan.volume["btc"]
                    trademan.sellAll("btc_jpy")
                    print("{date}\t{name}SELL ".format(**locals()) + "{0:+10.3f}\t{1:+5f}%".format(benefit, ratio))

        # 現在の価値
        print(date, end="\t")
        for trademan in traders:
            balance = trademan.getBalance()
            if balance >= last_balance[trademan.name]:
                print(Fore.GREEN + "{:10.3f}".format(balance) + Fore.RESET, end="  ")
            else:
                print(Fore.RED   + "{:10.3f}".format(balance) + Fore.RESET, end="  ")
            last_balance[trademan.name] = trademan.getBalance()
        print("|  ", end="")

        # 現在の価格
        for trademan in traders:
            rate = trademan.getRate("btc_jpy")
            if rate >= last_rate[trademan.name]:
                print(Fore.GREEN + "{:10.3f}".format(rate) + Fore.RESET, end="  ")
            else:
                print(Fore.RED   + "{:10.3f}".format(rate) + Fore.RESET, end="  ")
            last_rate[trademan.name] = trademan.getRate("btc_jpy")
        print("|  ", end="")

        # 最初の価格との差
        for trademan in traders:
            diff = last_rate[trademan.name] - first_rate[trademan.name]
            if diff >= 0:
                print(Fore.GREEN + "{:+10.3f}".format(diff) + Fore.RESET, end="  ")
            else:
                print(Fore.RED   + "{:+10.3f}".format(diff) + Fore.RESET, end="  ")
        print("|  ", end="")

        # 現在の価値 - 最初に買ってからホールドした時の金額
        for trademan in traders:
            diff = last_balance[trademan.name] - Capital * last_rate[trademan.name] / first_rate[trademan.name]
            if diff >= 0:
                print(Fore.GREEN + "{:+10.3f}".format(diff) + Fore.RESET, end="  ")
            else:
                print(Fore.RED   + "{:+10.3f}".format(diff) + Fore.RESET, end="  ")
        print("")
        time.sleep(9)

if __name__ == '__main__':
    main()