import json
import re

from flask import Flask, render_template, request
app = Flask(__name__)

from elasticsearch import Elasticsearch
es = Elasticsearch()

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    q_body = {
        'query': {
            'match': {
                'text': q
            }
        }
    }

    res = es.search(index='os', body=q_body)

    return json.dumps(
        [ r for r in generate_results(q, res) ]
    )

@app.route('/upload', methods=['POST'])
def upload():
    return 'NOT YET IMPLEMENTED'

# TODO: get more relevant results. Probably use some regex.
def generate_results(query, results):
    query_words = [ w.lower() for w in query.split()]

    for res in results['hits']['hits']:
        raw_text = res['_source']['text']
        words = raw_text.split()
        result_substr = []
        i = 0
        while i < len(words):
            word = words[i].lower()
            if word in query_words:
                left = min(i, 4)
                right = min(len(words) - i, 5)
                substr = ' '.join(words[i - left: i + right])
                result_substr.append(substr)
                i += right
            else:
                i += 1
        
        yield {
            'file': res['_source']['file'],
            'page': res['_source']['page'],
            'matches': result_substr
        }


