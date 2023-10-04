import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from graph_generator import Neo4jConnection

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

## QUERIES ##
# Create single Node
    # Note: Need to use parameters parameter to enter values
query = """
MERGE (c:Character {characterID: $characterID})
SET c += {
    firstName: $firstName,
    lastName: $lastName,
    age: $age,
    occupation: $occupation
}
"""

# Create a Relationship between 2 nodes
# query = """
# MATCH (a:Character {characterID: '1'}), (b:Character {characterID: '4'})
# CREATE (a)-[r:FRIENDS_WITH]->(b)
# RETURN type(r)
# """

# Read single node
# query = "MATCH (n) WHERE n.firstName = 'Tyler' RETURN n"

# Read all nodes
query = "MATCH (n) RETURN n"

# Update one node ###
# query = """MATCH (n:Character)
#         WHERE n.characterID = '4'
#         SET n.middleName = 'Michael'
#         RETURN n
# """

# Read the relationships
# query = """
# MATCH (a:Character {characterID: '1'})-[r:FRIENDS_WITH]-(b:Character)
# RETURN a, r, b
# """

# Delete node with specific id and without any relationships
    # Note: A node with a relationship can not be deleted.
# query = """
# MATCH (n:Character {characterID: '8'})
# DELETE n
# """

# Parameterless query
result = conn.query(query)

# Query with parameters
# result = conn.query(query, parameters={
#     'characterID': '11',
#     'firstName': 'Kira',
#     'lastName': 'Bednar',
#     'age': '32',
#     'occupation': 'Product Manager'
# })

# Process the result
for record in result:
    print(record)

# Close the connection
conn.close()

