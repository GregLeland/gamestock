
# Introduction

This project is based around getting real-time stock information and running a sentiment analysis on a recent major news article to see if there are any correlations between media coverage and current stock prices. It is currently a work in progress.

This project currently utilizes Python 3.x, NLTK's Vader Sentiment Intensity Analyzer, and web scraping with the Requests library and Beautiful Soup.


```python
import requests
from bs4 import BeautifulSoup as bs
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
```

## Importing Dependencies


```python
# LIST OF STOCK TICKERS FOR EACH GAME COMPANY
stockList = ['NTDOY',
             'EA',
             'UBSFY',
             'ATVI',
             'SGAMY',
             'TTWO',
             'SQNXF',
             'NCBDF']

# LIST OF GAME COMAPNIES
gcList = ['Nintendo',
          'Electronic Arts', 
          'Ubisoft',
          'Activision Blizzard',
          'Sega Sammy Holdings',
          'Take-two Interactive',
          'Square Enix',
          'Bandai Namco']
```

## Wrote a function to collect stock information


```python
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
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    source=requests.get(link, headers=headers).text
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
```

## Wrote a function to scrape an artice and its headline


```python
# ARTICLE INFO FUNCTION
def artInfo(company):
    # CREATE EMPTY DICTIONARY TO STORE INFORMATION
    gcDict = {}
    
    # URL CONFIG FOR FORBES
    link = f'https://www.forbes.com/search/?sort=recent&q={company}'
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    source=requests.get(link, headers=headers).text
    soup=bs(source,"html.parser")

    # SCRAPE THE FIRST HEADLINE AND LINK TO THE ARTICLE
    getHeadline=soup.find('a',class_="stream-item__title").text
    getLink=soup.findAll('a', {'class': 'stream-item__title'})[0]['href']   

    # SCRAPE THE ARTICLE DESCRIPTION
    getDesc = soup.find('div', class_='stream-item__description').text   
    
    # SCRAPE THE ARTICLE DATE
    getDate=soup.find('div',class_="stream-item__date").text
                  
    # COMPILE A DICTIONARY WITH INFO
    gcDict.update({'headline' : getHeadline} )
    gcDict.update( {'article_description' : getDesc} )
    gcDict.update( {'article_url' : getLink} )
    gcDict.update( {'article_date' : getDate} )

    return gcDict
```

## Wrote a function to run a sentiment analysis on the article and its headline


```python
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
```

## Passing the <span style="color:red">Nintendo</span> stock into the stock function and gathering the data


```python
# PASSING IN THE '0' INDEX FROM THE STOCK LIST, WHICH IS NINTENDO
myStock = stockInfo(stockList[0])
```


```python
company = myStock['company']
ticker = myStock['stock_ticker']
current_price = myStock['current_stock_price']
prev_close = myStock['previous_close']
stock_open = myStock['stock_open']
stock_vol = myStock['stock_volume']
avg_three_mo = myStock['avg_3month_volume']
avg_fify_two = myStock['52_week_range']
```


```python
nl = '\n'
summary = (f'Company: {company} {nl}'
           f'Ticker: {ticker} {nl}'
           f'Current Price: {current_price} {nl}'
           f'Previous Close: {prev_close} {nl}'
           f'Stock Open: {stock_open} {nl}'
           f'Stock Volume: {stock_vol} {nl}'
           f'3-month Average: {avg_three_mo} {nl}'
           f'52-week Average: {avg_fify_two}')
```


```python
print(summary)
```

    Company: Nintendo 
    Ticker: NTDOY 
    Current Price: 48.90 
    Previous Close: 48.43 
    Stock Open: 49.12 
    Stock Volume: 135,692 
    3-month Average: 286,053 
    52-week Average: 31.38 - 49.21
    

## Passing the Nintendo stock into the article and Natural Language Processing functions and gathering the data


```python
myNews = artInfo(company)
```


```python
myHeadline = myNews['headline']
myArticle = myNews['article_description']
myArtLink = myNews['article_url']
myArtDate = myNews['article_date']
mySentHead = SentAnal(myNews['headline'])
mySentBody = SentAnal(myNews['article_description'])
```


```python
sentiment = (f'Source: Forbes.com {nl}'
             f'Published: {myArtDate} {nl}'
             f'Article URL: {myArtLink} {nl}'
             f'{nl}'
             f'Headline: {myHeadline} {nl}'
             f'{nl}'
             f'Headline Sentiment Score: {mySentHead["overall_sentiment_score"]} {nl}'
             f'Overall Headline Sentiment: {mySentHead["input_sentiment_score"]} {nl}'
             f'{nl}'
             f'Article Snippit: {myArticle} {nl}'
             f'{nl}'
             f'Snippit Sentiment Score: {mySentBody["overall_sentiment_score"]} {nl}'
             f'Overall Snippit Sentiment: {mySentBody["input_sentiment_score"]} {nl}')
```


```python
print(sentiment)
```

    Source: Forbes.com 
    Published: 7 hours ago 
    Article URL: https://www.forbes.com/sites/davidthier/2019/09/18/the-legend-of-zelda-links-awakening-on-switch-release-date-and-5-things-to-know-before-you-play/ 
    
    Headline: 'The Legend Of Zelda: Link's Awakening' On Switch: Release Date And 5 Things To Know Before You Play 
    
    Headline Sentiment Score: 0.34 
    Overall Headline Sentiment: positive 
    
    Article Snippit: 'The Legend of Zelda: Link's Awakening' is nearly here. Here's the release date and five things to know before you play. 
    
    Snippit Sentiment Score: 0.34 
    Overall Snippit Sentiment: positive 
    
    

## Conclusion

At the moment, there is no way to come to a definitive conlusion, however, this project was crated as a proof of concept. In the future, I will be collecting a 30 days of stock data, articles from different sources that correlate with the day(s) the stock information was collected, and social media sentiment. In the very near future, I will also be creating interactive graphs that will visually illustrate the data.

Once this project is completed, I will be converting it to a Flask app with a HTML interface, where users can search for their own stocks and run their analysis.


```python

```
