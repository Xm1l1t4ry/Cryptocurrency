import plotly
import plotly.graph_objs as go
from plotly import tools
import re

def getName(line):
    res = re.split(r',', line, maxsplit=3)
    return res[2], res[3]

def getDate(line):
    res = re.split(r',', line, maxsplit=1)
    date = re.findall(r'\d{4}-\d{2}-\d{2}', res[0])
    return date[0], res[1]

def getVolume(line):
    res = re.split(r',', line, maxsplit=6)
    return res[5], res[6]

def getMarket(line):
    res = re.split(r',', line, maxsplit=1)
    return res[0]

def goMarketShare(dataset):
    markets = dict()
    for market in dataset:
        for date in dataset[market]:
            markets[market] = len(dataset[market][date])
    bar = go.Bar(x=list(markets.keys()), y=list(markets.values()))
    return bar

def goTradingVolume(dataset):
    currency = dict()
    for market in dataset:
        for date in dataset[market]:
            for val in dataset[market][date]:
                name, vol = [x for x in val]
                if name not in currency:
                    currency[name] = float(vol)
                else:
                    currency[name] += float(vol)
    pie = go.Pie(labels=list(currency.keys()), values=list(currency.values()))
    return pie

def goVolumeByDate(dataset):
    btc = dict()
    for market in dataset:
        for date in dataset[market]:
            for val in dataset[market][date]:
                name, vol = [x for x in val]
                if name == 'Bitcoin':
                    btc[date] = vol
    scatter = go.Scatter(x=list(btc.keys()), y=list(btc.values()))
    return scatter

def fileReader(path, limit):
    cryptos = dict()
    cnt = 0

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            first = file.readline().rstrip()

            header = [column.strip().lower() for column in first.split(',')]

            for line in file:
                if cnt <= limit:
                    name, new_line = getName(line)
                    date, new_line = getDate(new_line)
                    volume, new_line = getVolume(new_line)
                    market = getMarket(new_line)

                    if market not in cryptos:
                        cryptos[market] = dict()
                    if date not in cryptos[market]:
                        cryptos[market][date] = list()
                    cryptos[market][date].append([name, volume])
                    cnt+=1
            return cryptos
    except IOError as io_err:
        print(io_err.errno, io_err.strerror)
    except ValueError as val_err:
        print("Error in line", cnt, val_err)

a = fileReader('../data/crypto-markets.csv', 1000)

fig = tools.make_subplots(rows=1, cols=2)
fig.append_trace(goMarketShare(a), 1, 1)
fig.append_trace(goVolumeByDate(a), 1, 2)

plotly.offline.plot(fig, filename='DatasetPlot.html')
plotly.offline.plot([goTradingVolume(a)], filename='TradingVolume.html')