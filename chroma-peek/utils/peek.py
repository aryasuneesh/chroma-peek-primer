import chromadb 
import pandas as pd

class ChromaPeek:
    def __init__(self, path):
        self.client = chromadb.PersistentClient(path)

    ## function that returns all collection's names
    def get_collections(self):
        collections = []

        for i in self.client.list_collections():
            collections.append(i.name)
        
        return collections
    
    ## function to return documents/data inside the collection
    def get_collection_data(self, collection_name, dataframe=False):
        data = self.client.get_collection(name=collection_name).get()
        if dataframe:
            return pd.DataFrame(data)
        return data
    
    ## function to query the selected collection
    def query(self, query_str, collection_name, k=3, dataframe=False):
        collection = self.client.get_collection(collection_name)
        res = collection.query(
            query_texts=[query_str], n_results=min(k, len(collection.get()))
        )
        out = {}
        for key, value in res.items():
            if value:
                out[key] = value[0]
            else:
                out[key] = value
        if dataframe:
            return pd.DataFrame(out)
        return out
    
    ## function to delete selected rows from the collection
    def delete_rows(self, collection_name, ids=None):
        if ids:
            collection = self.client.get_collection(name=collection_name)
            collection.delete(ids=ids)
        else:
            raise ValueError("You must provide IDs to delete.")

