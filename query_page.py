## QUERIES ##
# Create single Node
    # Note: Need to use parameters parameter to enter values
ADD_SINGLE_NODE = """
MERGE (c:Character {characterID: $characterID})
SET c += {
    firstName: $firstName,
    lastName: $lastName,
    age: $age,
    occupation: $occupation
}
"""

# Create a Relationship between 2 nodes
ADD_RELATIONSHIP = """
MATCH (a:Character {characterID: '1'}), (b:Character {characterID: '4'})
CREATE (a)-[r:FRIENDS_WITH]->(b)
RETURN type(r)
"""

# Read single node
READ_ONE = "MATCH (n) WHERE n.firstName = 'Tyler' RETURN n"

# Read all nodes
READ_ALL = "MATCH (n) RETURN n"

# Read all relationships
READ_ALL_GRAPH_RELATIONSHIPS = """
MATCH (a:Character {characterID: '1'})-[r:FRIENDS_WITH]-(b:Character)
RETURN a, r, b
"""

# Read all relationships going both ways between node n and another node
# Also returns node n and any node node n has a relationship with
READ_NODE_RELATIONSHIPS = """
MATCH (n:Character)-[r]-(m)
WHERE n.characterID = '2'
RETURN r
"""

READ_OUTGOING_NODE_RELATIONSHIPS = """
MATCH (n:Character)-[r]-(m)
WHERE n.characterID = '2'
RETURN n, r, m
"""

READ_INCOMING_NODE_RELATIONSHIPS = """
MATCH (m)-[r]->(n:Character)
WHERE n.characterID = '2'
RETURN n, r, m
"""

# Update one node ###
UPDATE_NODE = """
MATCH (n:Character)
WHERE n.characterID = '4'
SET n.middleName = 'Michael'
RETURN n
"""

UPDATE_RELATIONSHIP = """
MATCH (n:Character {'characterID': '2'})-[r:HAS_APPEARANCE]->(m:PhysicalAppearance)
SET r += {
    status: 'current'
}
RETURN r
"""

# Delete node with specific id and without any relationships
    # Note: A node with a relationship can not be deleted.
DELETE_NODE = """
MATCH (n:Character {characterID: '8'})
DELETE n
"""