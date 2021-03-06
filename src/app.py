import os
from flask import Flask, render_template, request
from ranker.StructuredRanker import StructuredRanker
from ranker.PlainTextRanker import PlainTextRanker
import csv
import json

app = Flask(__name__)

index = 'indexes/indexNot Shortened.json'

structuredRanker = StructuredRanker(index)
plainTextRanker = PlainTextRanker(index)

unmap = lambda lista: [item for sublist in lista for item in sublist]
with open('indexes/name.csv') as documents:
    documents_list = unmap(list(csv.reader(open('indexes/name.csv'))))


def get_results_list(query, plain=True):
    if(plain):
        rank = plainTextRanker.getRank(query, tfIdf=False)
    else:
        rank = structuredRanker.getStructuredRank(query['title'], query['statement'], True)

    results_list = []
    for result in rank:
        obj = []
        document = json.load(open('retrieved/objects/{}.json'.format(documents_list[result[0]])))

        obj.append(format(documents_list[result[0]]).replace("http---", "http://").replace("https---", "https://").replace("-", "/"))
        obj.append(document['title'])
        obj.append(document['statement'][:300])
        results_list.append(obj)

    return results_list

@app.route('/', methods=['GET', 'POST'])
def index():
    # query_opts = {'plain_text': 'Plain Text', 'title': 'Title', 'statement': 'Statement'}
    if (request.method == "POST"):
        #plain search
        if ('plain' in request.form.keys()):
            text_query = request.form['query']
            data = get_results_list(text_query)
            # if(data is []):
            #     return render_template('results.html', titulo=titulo, msg="no results found")

            return render_template('results.html', data=data)
        #structured search
        elif('structured' in request.form.keys()):
            title_query = request.form['query_title']
            statement_query = request.form['query_statement']
            query={'title': title_query, 'statement':statement_query}
            data = get_results_list(query, plain=False)
            return render_template('results.html', data=data)


    return render_template('index.html')


if __name__ == '__main__':
    app.run()
