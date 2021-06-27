from pymongo import MongoClient


class MongoConnector(object):

    def __init__(self, _user='', _pass='', _ip='localhost', _port='27017', _dbname='test', _cl='test'):
        """
        Constructor for MongoConnector

        Args:
            _user (str):    Authentication username
            _pass (str):    Authentication password
            _ip (str):      Server ip-address
            _port (str):    Server port number
            _dbname (str):  Name o  f the database
            _cl (str):      Name of the collection
        """
        # Connect to the Mongo server
        self.client = MongoClient(
            "mongodb://{}:{}@{}:{}/?authSource={}".format(_user, _pass, _ip, _port, _dbname))

        # set the database and collection
        self.database = self.client[_dbname][_cl]

    def create(self, document):
        """
        Insert a document into the collection (Create Operation)

        Args:
            document (dict): Document to be inserted into collection

        Returns:
            object: document
        """
        if document.keys() is not None or document is not dict:
            self.database.insert_one(document)
            return True
        else:
            raise Exception('Failed to insert new document.')

    def readDocs(self, query):
        """
        Query documents from a database collection

        Args:
            query (dict):  Query parameters

        Returns:
            collection: Results from _query
        """
        if query is not None or query is not dict:
            result = self.database.find(query)
            return result
        else:
            raise Exception('Failed to parse query')

    def updateDocs(self, query_for, new_values, multiple_docs=False):
        """
        Update a document from a database collection using a query, and new values

        Args:
            query_for (dict): Query for matching documents
            new_values (dict): New values for each matching document
            multiple_docs (bool): (optional) pass True to update more than one document.

        Returns:
            bool: True if successful update, False if query is invalid or no documents were updated.
        """
        if query_for is not None and new_values is not None:
            if not multiple_docs:
                self.database.update(query_for, new_values)
                return True
            else:
                self.database.update(query_for, new_values)
                return True
        else:
            raise Exception('Failed to parse update query')

    def deleteDoc(self, query_for, multiple_docs=False):
        """
        Delete one or more documents matching a query

        Args:
            query_for (dict): Query for matching documents
            multiple_docs (bool): (optional) pass True to delete more than one document.

        Returns:
            bool: True if successful update, False if query is invalid or no documents were updated.
        """
        if query_for is not None:
            if not multiple_docs:
                result = self.database.delete_many(filter=query_for)
                return result.deleted_count > 0
            else:
                result = self.database.delete_one(filter=query_for)
                return result.deleted_count > 0
        else:
            raise Exception('Failed to parse delete query')

    def retrieveAllDocs(self):
        """
        Return all documents from database collection

        Returns:
            list: Every entry within the database's collection

        """
        return self.database.find({})

# end of MongoConnector class
