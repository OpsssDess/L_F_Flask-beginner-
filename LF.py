from flask import Flask, request, url_for, render_template
import json
import jinja2

app = Flask(__name__)
stock = []

@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route("/request/donation", methods=["POST"])
def donate():
    if request.form['name_stock'] == 'LIFO':
        stock.append({"name": request.form['name'],  "amount": int(request.form['amount'])})
    else:
        stock.insert(0,{"name": request.form['name'], "amount": int(request.form['amount'])})
    with open('good', 'w', encoding='utf-8') as f:
        json.dump(stock, f)
    return render_template('request_donation.html')

@app.route("/request/take", methods=["GET"])
def ask_good():
    with open('good', mode="r", encoding='utf-8') as file:
        stock1 = json.load(file)

    donation = {}

    if stock1:
        number_of_good = stock1[len(stock1) - 1]
        if number_of_good['amount'] == 1:
            donation = stock1.pop()
        else:
            number_of_good['amount'] -= 1
            donation = stock1[-1]

        with open('good', 'w', encoding='utf-8') as f:
            json.dump(stock1, f)

        return render_template('request_take.html', take_good=donation['name'])
    else:
        return render_template('request_take.html')


if __name__ == '__main__':
    app.run(debug=True)
