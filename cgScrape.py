import requests
import json
import numpy as np
import pandas as pd


def getData(url):
    test = requests.get(url)
    dict = json.loads(test.text)
    return dict


def scrapeData(coin, dfInput=None, outputFN=None):
    # get symbol name
    response = requests.get("https://api.coingecko.com/api/v3/coins/" + coin)
    symbol = json.loads(response.text)["symbol"]
    # 2020, 2021, 2022 until May 15th
    timeRange = [
        [1586563200, 1609344000],
        [1609430400, 1640880000],
        [1640966400, 1652544000],
    ]

    ranges = []

    for tr in timeRange:
        queryUrl = (
            "https://api.coingecko.com/api/v3/coins/"
            + coin
            + "/market_chart/range?vs_currency=usd&from="
            + str(tr[0])
            + "&to="
            + str(tr[1])
        )
        pulledData = getData(queryUrl)
        ranges.append(pulledData)

    if dfInput is None:
        df = pd.DataFrame(columns=[symbol + "Price", symbol + "MC", symbol + "TV"])
    else:
        df = dfInput
        df[symbol + "Price"] = np.zeros(len(df))
        df[symbol + "MC"] = np.zeros(len(df))
        df[symbol + "TV"] = np.zeros(len(df))

    if dfInput is None:
        for values in ranges:
            # putting initial data in dataframes
            initialDf = pd.DataFrame(
                values["prices"], columns=["timestamp", symbol + "Price"]
            )
            initialDf.set_index("timestamp", inplace=True)
            df = pd.concat([df, initialDf])

    # df[symbol + "MC"] = np.zeros(len(df))
    # df[symbol + "TV"] = np.zeros(len(df))
    print(len(df))

    for values in ranges:
        for item in values["market_caps"]:
            df.at[item[0], symbol + "MC"] = item[1]
        print("market caps done")

        for item in values["total_volumes"]:
            df.at[item[0], symbol + "TV"] = item[1]
        print("total volumes done")

        if not dfInput is None:
            for item in values["prices"]:
                df.at[item[0], symbol + "Price"] = item[1]
            print("prices done")
    df.sort_index
    if not outputFN is None:
        df.to_csv(outputFN)
        print(df.head)
        print("Scrape Completed")
    return df

