import json
import requests
import datetime
import pytz
from flask import Flask, app
from flask import render_template
from flask import request
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def GetStockInfo():

    if request.method == 'POST':
        stockSymbol = request.form['symbol']
        try :
            pacific_time_zone = pytz.timezone('US/Pacific')
            time_format = "%a %b %d %H:%M:%S %Z %Y"
            pacific_time = datetime.datetime.now(pacific_time_zone)
            formatted_pacific_time = pacific_time.strftime(time_format)

            dataResult = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+stockSymbol+'&apikey=249M9Y8XLLHNRLZI')
            data = dataResult.json()
            symbol = data['Global Quote']['01. symbol']
            price = data['Global Quote']['05. price']
            change = data['Global Quote']['09. change']
            changePercent = data['Global Quote']['10. change percent']

            stockNameResult = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+stockSymbol+'&apikey=249M9Y8XLLHNRLZI')
            stockName = stockNameResult.json()['bestMatches'][0]['2. name']
            data = {'ticketSymbol': symbol, 'stockprice': price,
                        'change': change, 'changePercent': changePercent,
                        'time': formatted_pacific_time, 'fullname' : stockName
                        }
            return render_template('index1.html', data=data)
        except:
            return render_template('index1.html', error ={'error' : 'Unable to retrive data for '  + stockSymbol})

    return render_template('index1.html')

if __name__ == '__main__':
    #GetStockInfo('AAPL')
    app.run(debug=True, host='0.0.0.0')
