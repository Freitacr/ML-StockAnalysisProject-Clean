'''
Created on Nov 27, 2018

@author: Colton Freitas
@summary: 

Contains the base methods for downloading data from the data sources
These methods will call further sub methods to accomplish their tasks
that are not needed to be visible for the calling method(s)
'''

from Download.YahooDataDownloader import getCookieAndCrumb, buildURL, getDataFromURL
from urllib.error import HTTPError, URLError
from Data.Structures.SharedDataStorageClasses import SourceDataStorage
from Download.GlobalDownloadLogger import getLogger
from datetime import datetime as dt



def DownloadDataYahoo (tickerList):
    '''Downloads Stock Data from Yahoo
        @param tickerList: The list of stock tickers to obtain data for
        @type tickerList: Array of Strings
        @return Storage object containing obtained data
        @rtype: SourceDataStorage
    '''
    logger = getLogger()
    dataStorage = SourceDataStorage("Yahoo")
    cookie, crumb = [None, None]
    try:
        cookie, crumb = getCookieAndCrumb()
    except HTTPError as e:
        logger.logException(e)
        logger.logWarning("Error is irrecoverable for Downloading Yahoo Data, skipping...")
        return dataStorage
    except URLError as e:
        logger.logException(e)
        logger.logWarning("Error is irrecoverable, and may be the result of trouble establishing a connection. Skipping yahoo downloading.")
        return dataStorage

    for ticker in tickerList:
        today = dt.now()
        downloadURL = buildURL(ticker, 0, round(today.timestamp()), crumb)
        tickerDataStorage = None
        try:
            tickerDataStorage = getDataFromURL(downloadURL, ticker, cookie)
        except HTTPError as e:
            logger.logException(e)
            logger.logWarning("Error retrieving data for {0}, skipping...".format(ticker))
            continue
        except URLError as e:
            logger.logException(e)
            logger.logWarning("Error retrieving data for {0}, skipping...".format(ticker))
            continue
        dataStorage.addTickerDataStorage(tickerDataStorage)
    return dataStorage
    
def DownloadDataGoogle (tickerList):
    '''Downloads Stock Data from Google
        @param tickerList: The list of stock tickers to obtain data for
        @type tickerList: Array of Strings
        @return Storage object containing obtained data
        @rtype: StockDataStorage
        @status: Not Implemented
    '''    
    pass;