import os
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input 
from elasticsearch import Elasticsearch
from utils import FeatureExtractor

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--index', type=str, default='image')
args = parser.parse_args()

app = Flask(__name__)
fe = FeatureExtractor()
es = Elasticsearch('es:9200')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=["POST"])
def query():
    f = request.files['query_image']
    image = Image.open(f.stream)
    image.save(f.filename)

    image = image.resize((224, 224))
    query_vector = fe.extract(image)

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc.vector) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    res = es.search(
        index=args.index,
        body={
            "size": 5,
            "query": script_query,
        }
    )
    res = [{'rank':idx+1, 'path':i['_source']['path'], 'score':i['_score']} for idx,i in enumerate(res['hits']['hits'])]
    return render_template('result.html', query=f.filename, result=res)

@app.route('/image/<path:filename>')
def image(filename):
    return send_from_directory(app.root_path, filename)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port=5000, 
        debug=True
    )