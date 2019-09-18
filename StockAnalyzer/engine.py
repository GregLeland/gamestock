# IMPORTS
import requests
from bs4 import BeautifulSoup as bs
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


# STOCK INFO FUNCTION
def stockInfo(stock):
    stockDict = {}
    if stock == 'NTDOY':
        stockDict.update( {'company' : 'Nintendo'} )
    elif stock == 'EA':
        stockDict.update( {'company' : 'Electronic Arts'} )
    elif stock == 'UBSFY':
        stockDict.update( {'company' : 'Ubisoft'} )
    elif stock == 'ATVI':
        stockDict.update( {'company' : 'Activision Blizzard'} )
    elif stock == 'SGAMY':
        stockDict.update( {'company' : 'Sega Sammy Holdings'} )
    elif stock == 'TTWO':
        stockDict.update( {'company' : 'Take-two Interactive'} )
    elif stock == 'SQNXF':
        stockDict.update( {'company' : 'Square Enix'} )
    elif stock == 'NCBDF':
        stockDict.update( {'company' : 'Bandai Namco'} )
            
    # URL CONFIG FOR YAHOO FINANCE
    link = f'https://finance.yahoo.com/quote/{stock}?p={stock}&.tsrc=fin-srch'
    #headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    source=requests.get(link).text
    soup=bs(source,"html.parser")
    
    # SCRAPE THE STOCK INFORMATION
    stockPrice = soup.find('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text.strip()
    marketCap = soup.find('td', {'data-test':"MARKET_CAP-value"}).span.text
    stockPrevious = soup.find('td', {'data-test':"PREV_CLOSE-value"}).span.text
    stockOpen = soup.find('td', {'data-test':"OPEN-value"}).span.text
    stockVolume = soup.find('td', {'data-test':"TD_VOLUME-value"}).span.text
    avg3moVolume = soup.find('td', {'data-test':"AVERAGE_VOLUME_3MONTH-value"}).span.text
    ftWeekRange = soup.find('td', {'data-test':"FIFTY_TWO_WK_RANGE-value"}).text
    
    # UPDATE STOCK DICTIONARY WITH COMPANY NAME AND STOCK INFO
    stockDict.update( {'stock_ticker' : stock} )
    stockDict.update( {'current_stock_price' : stockPrice} )
    stockDict.update( {'market_cap' : marketCap} )
    stockDict.update( {'previous_close' : stockPrevious} )
    stockDict.update( {'stock_open' : stockOpen} )
    stockDict.update( {'stock_volume' : stockVolume} )
    stockDict.update( {'avg_3month_volume' : avg3moVolume} )
    stockDict.update( {'52_week_range' : ftWeekRange} )
    
    return stockDict

# ARTICLE INFO FUNCTION
def artInfo(company):
    # CREATE EMPTY DICTIONARIES TO STORE INFORMATION
    gcDict = {}
    
    # URL CONFIG FOR FORBES
    link = f'https://www.forbes.com/search/?q={company}'
    #headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    source=requests.get(link).text
    soup=bs(source,"html.parser")

    # SCRAPE THE FIRST HEADLINE AND LINK TO THE ARTICLE
    getHeadline=soup.find('a',class_="stream-item__title").text
    getLink=soup.findAll('a', {'class': 'stream-item__title'})[0]['href']   

    # SCRAPE THE ARTICLE DESCRIPTION
    getDesc = soup.find('div', class_='stream-item__description').text   
                  
    # COMPILE A DICTIONARY WITH INFO
    gcDict.update({'headline' : getHeadline} )
    gcDict.update( {'article_description' : getDesc} )
    gcDict.update( {'article_url' : getLink} )

    return gcDict

# SENTIMENT ANALYSIS
def SentAnal(sentFeed):
    sentDict = {}
    sentAnalysis = {}
    sia = SIA() 
    sent_score = sia.polarity_scores(sentFeed)
    sentAnalysis.update(sent_score)
    finalScore = sentAnalysis['compound']
    sentDict.update({'overall_sentiment_score' : finalScore})
    sentDict.update( {"input_sentiment_score": 
        "positive" if finalScore > 0.28 else 
        "negative" if finalScore < -0.28 else 
        "neutral"
    })
    return sentDict