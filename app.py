from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':


        symbol = request.form['symbol']
        allotment = float(request.form['allotment'])
        final_share_price = float(request.form['final_share_price'])
        sell_comm = float(request.form['sell_comm'])
        init_share_price = float(request.form['init_share_price'])
        buy_comm = float(request.form['buy_comm'])
        cap_gain_tax = float(request.form['cap_gain_tax'])

        proceeds = int(allotment) * float(final_share_price)
        total_tax = (((float(final_share_price) - float(init_share_price)) * int(allotment) - float(buy_comm) - float(sell_comm)))
        tax = total_tax * float(cap_gain_tax) / 100
        init_total = int(allotment) * float(init_share_price)
        cost = init_total + float(buy_comm) + float(sell_comm) + tax
        netProfit = proceeds - cost
        return_on_inv = netProfit / cost * 100
        breakeven = (init_total + float(buy_comm) + float(sell_comm)) / int(allotment)
        proceeds = "$%.2f" % proceeds
        cost = "$%.2f" % cost
        init_total = str(allotment) + " x $" + str(init_share_price) + " = %.2f" % init_total
        gainFormat = str(cap_gain_tax) + "% of $" + "%.2f" % total_tax + " = %.2f" % tax
        netProfit = "$" + "%.2f" % netProfit
        return_on_inv = "%.2f" % return_on_inv + "%"
        breakeven = "$" + "%.2f" % breakeven
        tempData = {'tickerSymbol': symbol, 'allot': allotment,
                   'finalShare': final_share_price, 'sellComm':sell_comm,
                   'initShare':init_share_price, 'buyComm':buy_comm,
                   'taxRate':cap_gain_tax, 'proceeds':proceeds,
                   'cost':cost, 'init_total': init_total, 'netProfit':netProfit,
                   'ret_on_inv':return_on_inv, 'breakeven':breakeven}
        return render_template('index.html', **tempData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
