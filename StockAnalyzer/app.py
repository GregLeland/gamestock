from flask import Flask, jsonify, Response, render_template, request, redirect, url_for
import json
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SubmitField, validators
from engine import *
import requests

app = Flask(__name__)
app.static_folder = 'static'

# CREATE A SECRET KEY BECAUSE THE STUPID FORM REQUIRES IT FOR VALIDATION
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# INDEX ROUTE - 
# ALSO LISTENS FOR THE POST FROM THE AUTOCOMPLETE FORM AND ROUTES THE FORM SUBMISSION TO THE STOCK ROUTE
@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST':
        form_cont = form.autocomp.data.replace(" ", "%20")
        return redirect('http://stocksentiment.herokuapp.com/stock/' + form_cont)
    gameco = []
    for x in stockList:
        gameco.append(x)
        print(x)
    return render_template('index.html', form=form, gameco=gameco)

@app.route("/stock/<title>", methods=['GET', 'POST'])
def stockinfo(title):
    form = SearchForm(request.form)
    if request.method == 'POST':
        form_cont = form.autocomp.data.replace(" ", "%20")
        return redirect('http://stocksentiment.herokuapp.com/stock/' + form_cont)
    myStock = stockInfo(title)
    company = myStock['company']
    ticker = myStock['stock_ticker']
    current_price = myStock['current_stock_price']
    prev_close = myStock['previous_close']
    stock_open = myStock['stock_open']
    stock_vol = myStock['stock_volume']
    avg_three_mo = myStock['avg_3month_volume']
    avg_fify_two = myStock['52_week_range']
    myNews = artInfo(company)
    myHeadline = myNews['headline']
    myArticle = myNews['article_description']
    myArtLink = myNews['article_url']
    mySentHead = SentAnal(myNews['headline'])
    mySentBody = SentAnal(myNews['article_description'])
    pageImageURL = f'img/{ticker}.jpg'
    return render_template('stock.html', 
                            myStock=myStock,
                            mySentHead=mySentHead,
                            mySentBody=mySentBody,
                            myArticle=myArticle,
                            myHeadline=myHeadline,
                            myArtLink=myArtLink,
                            company=company,
                            ticker=ticker,
                            current_price=current_price,
                            prev_close=prev_close,
                            stock_open=stock_open,
                            stock_vol=stock_vol,
                            avg_three_mo=avg_three_mo,
                            avg_fify_two=avg_fify_two,
                            pageImageURL=pageImageURL,
                            form=form)

# SETS UP THE FORM WITH THE AUTOCOMP TEXT FIELD AND SUBMISSION BUTTON
class SearchForm(Form):
    autocomp = TextField('Enter Stock Ticker', id='stock_autocomplete')
    submit = SubmitField('Search')

# THE BRAINS OF THE AUTOCOMPLETE. PULLS THE STOCK TICKERS FROM THE LIST VARIABLE AND RETURNS A JSON THAT CAN BE PARSED BY THE JQUERY ON THE HTML PAGE
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(stockList), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)