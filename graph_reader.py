import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from graph_connector import Neo4jConnection
import query_page

load_dotenv()

NEO_USERNAME = os.getenv("NEO_USERNAME")
NEO_PASSWORD = os.getenv("NEO_PASSWORD")
NEO_URI = os.getenv("NEO_URI")

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__password = pwd
        self.__driver = None
        
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print("Failed to create the driver: ", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver is not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query faild: ", e)
        finally:
            if session is not None:
                session.close()
        return response
    
# Connect to Neo4j
conn = Neo4jConnection(uri=NEO_URI, user=NEO_USERNAME, pwd=NEO_PASSWORD)

# Parameterless query
result = conn.query(query_page.READ_ALL_GRAPH_RELATIONSHIPS)

# Process the result
for record in result:
    print(record)

# Close the connection
conn.close()

