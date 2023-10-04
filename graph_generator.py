import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO_USERNAME = os.getenv("NEO_USERNAME")
NEO_PASSWORD = os.getenv("NEO_PASSWORD")
NEO_URI = os.getenv("NEO_URI")

def load_json(filename):
    script_dir = os.path.dirname('/Users/brendansmith/Documents/StarbucksHollow/')
    file_path = os.path.join(script_dir, filename)

    i = 0
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['characters']
        # for character in data['characters']:
        #     i += 1
        #     print("#####CHARACTER: ", i, '#####')
        #     print(character)

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))

    def close(self):
        self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed: ", e)
        finally:
            if session is not None:
                session.close()
        return response
    
# conn = Neo4jConnection(uri=NEO_URI, user=NEO_USERNAME, pwd=NEO_PASSWORD)

# characters = load_json('characters.json')
# print(characters)

# for character in characters:
#     character_query = """
#     MERGE (c:Character {characterID: $characterID})
#     SET c += {
#         firstName: $firstName,
#         lastName: $lastName,
#         age: $age,
#         occupation: $occupation
#     }
#     """
#     conn.query(character_query, parameters={
#         'characterID': character['characterID'],
#         'firstName': character['name']['firstName'],
#         'lastName': character['name']['lastName'],
#         'age': character['age'],
#         'occupation': character['occupation']
#     })

# conn.close()
