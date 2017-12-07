import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # query_opts = {'plain_text': 'Plain Text', 'title': 'Title', 'statement': 'Statement'}
    if (request.method == "POST"):
        #plain search
        if ('plain' in request.form.keys()):
            print("plain search")
        #structured search
        elif('structured' in request.form.keys()):
            pass



            # select_opt = request.form.get('query_select')
            # text_query = request.form['query']
            # title_query = request.form['query_title']
            # statement_query = request.form['query_statement']
            # print(text_query)
            # print(title_query)
            # print(statement_query)
            # print(str(select_opt))


            # button_plain = request.form['plain']
            # print(button_plain)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
