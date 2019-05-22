import azure.cosmos.cosmos_client as cosmos_client

class DataAccess():

    def __init__(self,dbUrl,masterKey,databaseName):     
        self.client = cosmos_client.CosmosClient(url_connection=dbUrl, auth={'masterKey': masterKey})
        self.databaseName = databaseName
       
    #function to read records from mongo db
    def findAll(self, collectionName):
        try:
            database_link = 'dbs/' + self.databaseName
            collection_link = database_link + '/colls/' + collectionName
            documentlist = list(self.client.ReadItems(collection_link))
            return documentlist

        except Exception as e:
            print(str(e))
     
    
