from elasticsearch import Elasticsearch
import argparse

from create_documents import encoding
  

def main(args):
    """Searches the query in the index and returns the result"""
    es = Elasticsearch(args.host)
    query_vector = encoding(args.text)

    resp = es.search(
    index=args.index_name,
    size=10,
    query = {
    "match": {
      "src": 
        {"query": args.text,
        "boost": 0.3}
            }
            },
    knn = {
    "field": "src_token",
    "k": 10,
    "num_candidates": 100,
    "query_vector": query_vector,
    "similarity": 0.9,
    "boost": 0.5,
        },
    min_score=0.5,
    fields=["id", "src", "tran"]   ,
    _source=False,
    ignore=[400]      
    )
    res = []

    for hit in resp.body["hits"]["hits"]:
        print("result: ", hit["fields"]["src"], " score: ", hit["_score"])
        res.append({"result": hit["fields"]["src"], "score": hit["_score"]})

    return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--text', default='I can feel it', help='input text.')
    parser.add_argument('--host', default='http://localhost:9200/', help='elasticsearch host.')
    parser.add_argument('--index_name', default="tran_memory", help='name of es index.')
    args = parser.parse_args()
    main(args)