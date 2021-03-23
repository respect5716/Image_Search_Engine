import os
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
from utils import create_model, Dataloader
from PIL import Image

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--p', type=int, default=9200)
parser.add_argument('--index', type=str, default='image')
args = parser.parse_args()

def create_index(es, index):
    mapping = {
        "mappings": {
            "properties": {
                "path": {"type": "text"},
                "vector": {"type": "dense_vector", "dims": 1280}
            }
        }
    }
    es.indices.create(index=index, body=mapping)
    print("Creating index complete")


def main(args):
    es = Elasticsearch(f'es:{args.p}')
    create_index(es, args.index)
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    loader = Dataloader(image_dir, 32)
    model = create_model()


    for i in tqdm(range(len(loader))):
        path, image = loader.__getitem__(i)
        vector = model.predict(image)
        docs = [{'_index':args.index, '_source':{'path':str(p), 'vector':list(v)}} for p,v in zip(path, vector)]
        helpers.bulk(es, docs)
    
    print("Preparing complete")


if __name__ == '__main__':
    main(args)