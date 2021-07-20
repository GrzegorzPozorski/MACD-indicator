import pandas as pd
import re
import matplotlib.pyplot as plt
import sys

FILE = 'csv/tesla_5_years.csv'
ROUNDING = 0


def prepare_samples(NROFSAMPLE):
    PRICES = []
    col = 1    # column with interasting data
    df = pd.read_csv(FILE)

    column = df.iloc[:, col]

    for price in column:
        tmp = re.findall(r'\d+(?:\.\d+)?', price)
        if tmp:
            PRICES.append(float(tmp[0]))

    cur_nr_of_samples = NROFSAMPLE
    N = 26  # nr of periods
    if len(PRICES) < cur_nr_of_samples + N:
        if len(PRICES) > N:
            cur_nr_of_samples = len(PRICES) - N
        else:
            print("not enough data (less than " + str(NROFSAMPLE) + ")!")
            sys.exit()

    PRICES.reverse()

    return PRICES, cur_nr_of_samples   # array 'PRICES' sorted from oldest


def calc_EMA(PRICES, N):
    EMA = []
    a = 2/(N+1)  # alpha

    for i in range(0, len(PRICES)-1-N):
        # taking current N periods
        cur_prices = PRICES[i:i+N+1]

        numerator = 0.0
        denominator = 0.0
        exponent = 0

        for j in range(N, -1, -1):
            numerator += cur_prices[j]*(pow(1-a, exponent))
            denominator += pow(1-a, exponent)
            exponent += 1

        EMA.append(numerator/denominator)

    return EMA


def calc_MACD(EMA12, EMA26):
    EMA12.reverse()
    EMA26.reverse()
    MACD = []
    for i in range(0, len(EMA26)):
        MACD.append(EMA12[i] - EMA26[i])
    MACD.reverse()

    return MACD


def take_NROFSAMPLE(MACD, SIGNAL, PRICES):

    MACD = MACD[len(MACD) - NROFSAMPLE:]
    SIGNAL = SIGNAL[len(SIGNAL) - NROFSAMPLE:]
    PRICES = PRICES[len(PRICES) - NROFSAMPLE:]

    return MACD, SIGNAL, PRICES


def buy(currentStockPrice, stocks, wallet, howMany):
    stocks += (wallet*howMany)/currentStockPrice
    stocks = round(stocks, ROUNDING)
    wallet = wallet*(1.0 - howMany)
    return stocks, wallet


def sell(currentStockPrice, stocks, wallet, howMany):
    wallet += (stocks*howMany)*currentStockPrice
    wallet = round(wallet, ROUNDING)
    stocks = stocks*(1.0 - howMany)
    return stocks, wallet


def draw_chart(MACD, SIGNAL, PRICES):

    plt.plot(list(range(0, NROFSAMPLE)), PRICES, label='stock price')
    plt.plot(list(range(0, NROFSAMPLE)), MACD, label='MACD')
    plt.plot(list(range(0, NROFSAMPLE)), SIGNAL, label='SIGNAL')
    plt.legend()


def simulation(MACD, SIGNAL, PRICES, NROFSAMPLE, stocks, wallet):

    draw_chart(MACD, SIGNAL, PRICES)

    bought = False

    for i in range(0, NROFSAMPLE):
        howMany = 1.0   # small improvement - buy/sell partly
        if SIGNAL[i] < MACD[i]:
            if not bought:
                if MACD[i] > 0:
                    howMany = 0.5

                stocks, wallet = buy(PRICES[i], stocks, wallet, howMany)
                bought = True
                mark_points(i, SIGNAL, PRICES, 'green')

        elif SIGNAL[i] > MACD[i]:
            if bought:
                if MACD[i] > 0:
                    howMany = 0.5

                stocks, wallet = sell(PRICES[i], stocks, wallet, howMany)
                bought = False
                mark_points(i, SIGNAL, PRICES, 'red')

    ending_money = round(PRICES[NROFSAMPLE-1] * stocks + wallet, ROUNDING)

    return ending_money


def mark_points(i, SIGNAL, PRICES, color):
    plt.scatter(i, SIGNAL[i], s=13, c=color)
    plt.scatter(i, PRICES[i], s=13, c=color)
    plt.axvline(i, 0, 1, ls=':', lw=0.5, c=color)


def print_results(ending_money, starting_money, starting_stocks, ending_price, ROUNDING):

    profit1 = round(((ending_money - starting_money) / starting_money) * 100, ROUNDING)
    profit2 = round(((starting_stocks * ending_price - starting_money) / starting_money) * 100, ROUNDING)
    print("assets at the beginning: " + str(starting_money))
    print("assets after investing with algorithm: " + str(ending_money) + ", " + str(profit1) + "% profit/loss")
    print("assets after one-time purchase at beginning and holding all stocks: " + str(
        starting_stocks * ending_price) + ", " + str(profit2) + "% profit/loss")


if __name__ == '__main__':

    # calculations
    NROFSAMPLE = 1000
    PRICES, NROFSAMPLE = prepare_samples(NROFSAMPLE)
    MACD = calc_MACD(calc_EMA(PRICES, 12), calc_EMA(PRICES, 26))
    SIGNAL = calc_EMA(MACD, 9)
    MACD, SIGNAL, PRICES = take_NROFSAMPLE(MACD, SIGNAL, PRICES)

    # situation at the beginning
    stocks = 0
    wallet = 1000
    starting_money = wallet
    starting_stocks = round(wallet/PRICES[0], ROUNDING)

    # simulation
    ending_money = simulation(MACD, SIGNAL, PRICES, NROFSAMPLE, stocks, wallet)

    # results
    print_results(ending_money, starting_money, starting_stocks, PRICES[NROFSAMPLE-1], ROUNDING)
    plt.show()

