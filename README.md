# ragmonopoly

### Never get tricked by your friends :D 
Ask questions about monopoly, and get response!

All free, in your local machine.

Script utilizes nomic-embeddings, and mistral for generation, and chromadb for as vector database

PS: This project is made for fun purposes


to run the script
1. run
```console
python database_manager.py
    
# to reset the database and clear up run
database_manager.py --reset
    
```

2. now vector database is created, we can run query with our prompt
```console
python query_data.py 'what happens if I end up in jail?'
```

   
