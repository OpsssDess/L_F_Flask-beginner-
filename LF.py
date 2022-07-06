from flask import Flask, request, url_for
import json

app = Flask(__name__)
stock = []

@app.route('/')
def main_page():
    return """<html>
                    <body>
                        <section>
                            <h2>Регистрация прошения</h2>
                                <p>
                                    <form action="/request/take" method="get">
                                    <button type="submit">Взять.</button>
                                    </form>
                                </p>
                        </section>
                        <section>
                            <h2>Регистрация пожертвования</h2>
                                <p>
                                    <form action="/request/donation" method="post">
                                    <label for="name">Какую вещь хотите отдать?</label>
                                    <input type="text" name="name">
                                    <label for="name">Сколько штук?</label>
                                    <input type="text" name="amount">
                                    <label for="name">Куда хотите положить (FIFO or LIFO?</label>
                                    <input type="text" name="name_stock">
                                    <button type="submit">Отправить</button>
                                    </form>
                                </p>
                        </section>
                    </body>
                </html>"""


@app.route("/request/donation", methods=["POST"])
def donate():
    if request.form['name_stock'] == 'LIFO':
        stock.append({"name": request.form['name'],  "amount": int(request.form['amount'])})
    else:
        stock.insert(0,{"name": request.form['name'], "amount": int(request.form['amount'])})
    with open('good', 'w', encoding='utf-8') as f:
        json.dump(stock, f)
    return f"""<html>
                    <body>
                        <section>
                            <h2>Спасибо!!!</h2>
                                <a href="{url_for('main_page')}">Вернуться на главную</a>
                        </section>
                    </body>
                </html>"""


@app.route("/request/take", methods=["GET"])
def ask_good():
    with open('good', mode="r", encoding='utf-8') as file:
        stock1 = json.load(file)

    if stock1:
        number_of_good = stock1[len(stock1) - 1]
        if number_of_good['amount'] == 1:
            donation = stock1.pop()
        else:
            number_of_good['amount'] -= 1
            donation = stock1[-1]

        with open('good', 'w', encoding='utf-8') as f:
            json.dump(stock1, f)

        return f"""<html>
                        <body>
                            <section>
                                <h2>Подойдите к окну</h2>
                                    <p>Возьмите {donation['name']}, в количестве 1</p>
                                    <a href="{url_for('main_page')}">Вернуться на главную</a>
                            </section>
                        </body>
                    </html>"""
    else:
        return f"""<html>
                    <body>
                        <section>
                            <h2>Подойдите к окну</h2>
                                <p>Сейчас на складе ничего нет</p>
                                <a href="{url_for('main_page')}">Вернуться на главную</a>
                        </section>
                    </body>
                </html>"""


if __name__ == '__main__':
    app.run(debug=True)
