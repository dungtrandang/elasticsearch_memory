Steps:
- Install elasticseach
- Set up environment using `env.yaml` file
- Create elasticsearch cluster => connect to cluster to start service
- Prepare data: connect data source and edit the `create_documents` function in `create_documents.py` file to pass each pair of `source` and `translation` to `documents` class. The current code work for file `data.json`
- Prepare mapping for ES: `config/index.json`
- Run:
```Terminal
python create_documents.py --index_name <name of index in ES> --index_path <path to mapping file, e.g config/index.json> 
python search.py --host <ES host> --text <input text to search> --index_name <index name>
```