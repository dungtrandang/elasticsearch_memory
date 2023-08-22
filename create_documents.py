import json
import argparse
from tqdm import tqdm
from transformers import BertTokenizer
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk



def encoding(text):
    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    encoded_text = tokenizer.encode(text, 
                            padding='max_length', 
                            truncation=True, 
                            max_length = 768, 
                            add_special_tokens = True)
    norm = np.linalg.norm(encoded_text)
    if norm == 0:
        return encoded_text
    return encoded_text/norm


class documents():
    src : str = ""
    tran : str = ""
    src_token : any
    tran_token : any

    def __init__(self, src, tran):
        self.src = src
        self.tran = tran
        self.src_token = encoding(src)
        self.tran_token = encoding(tran)

# Load the data and create documents
def create_documents(data_path='data.json'):
    with open(data_path) as f:
        dataset = json.load(f)
    for data in dataset:
        document = documents(
            data['translation']['en'], 
            data['translation']['vi'])
        yield document.__dict__
    
def create_index(els_instance,
                 index_path='config/index.json', 
                 index_name='tran_memory' 
                 ):

    with open(index_path,'r') as f:
        index = json.load(f)
        mappings = index['mappings']
        settings = index['settings']
    
    els_instance.indices.create(index=index_name, mappings=mappings, settings=settings)

def main(args):

    data_path=args.data_path
    index_path=args.index_path
    index_name=args.index_name
    host=args.host
    # collect len data for tqdm, if using external data source, 
    # remove this code (open data file and count data), pass len_data here
    with open(data_path) as f:
        dataset = json.load(f)
    len_data = len(dataset)

    # create documents generator
    document_generator = create_documents('data.json')
    
    # create index
    es = Elasticsearch(host)
    if not es.indices.exists(index=index_name):
        create_index(es, index_path, index_name)
    
    # index documents
    if args.index_bulk:
        bulk(es, document_generator, index=index_name)
    else: 
        # number of documents for indexing if only testing with small data. 
        # Set to len_data if indexing all data       
        num_for_index = 500 
        if len_data < num_for_index:
            num_for_index = len_data
        for i, document in tqdm(enumerate(document_generator), total=num_for_index):
            if i < num_for_index:
                es.index(index=index_name, id=i, document=document)
            else:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexing elasticsearch documents.')
    parser.add_argument('--data_path', default='data.json', help='data path.')
    parser.add_argument('--index_path', default='config/index.json', help='mapping path.')
    parser.add_argument('--index_name', default='tran_memory', help='index name.')
    parser.add_argument('--host', default='http://localhost:9200/', help='elasticsearch host.')
    parser.add_argument('--index_bulk', default=False, help='index bulk or not.')
    args = parser.parse_args()
    main(args)