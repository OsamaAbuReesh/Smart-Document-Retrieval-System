from flask import Flask, render_template, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}], basic_auth=('osama', 'osama123'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_query = request.args.get('query')

    # Your Elasticsearch query
    es_query = {
        "query": {
            "match": {
                "title": {
                    "query": search_query,
                    "fuzziness": "2",
                    "analyzer": "title_analyzer"
                }
            }
        }
    }

    result = es.search(index='reuter_index', body=es_query)
    suggestions = [hit['_source']['title'] for hit in result['hits']['hits']]

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)