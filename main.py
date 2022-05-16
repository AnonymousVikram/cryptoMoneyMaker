import pandas as pd
from cgScrape import scrapeData


def main():    
    tempDf = scrapeData("solana")
    tempDf = scrapeData("bitcoin", tempDf)
    scrapeData("ethereum", tempDf, "scrapedData.csv")

main()