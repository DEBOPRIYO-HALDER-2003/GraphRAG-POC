CREATE_DOCUMENT = """
MERGE (d:Document {
    id:$document_id
})
SET d.filename=$filename
RETURN d
"""

CREATE_CHUNK = """
MERGE (c:Chunk {
    id:$chunk_id
})
SET
    c.text=$text,
    c.chunk_index=$chunk_index

RETURN c
"""

LINK_DOCUMENT_CHUNK = """
MATCH (d:Document {
    id:$document_id
})

MATCH (c:Chunk {
    id:$chunk_id
})

MERGE (d)-[:HAS_CHUNK]->(c)
"""

CREATE_ENTITY = """
MERGE (e:Entity {
    name:$name
})
SET e.type=$type
RETURN e
"""

LINK_CHUNK_ENTITY = """
MATCH (c:Chunk {
    id:$chunk_id
})

MATCH (e:Entity {
    name:$entity_name
})

MERGE (c)-[:MENTIONS]->(e)
"""

CREATE_RELATIONSHIP = """
MATCH (a:Entity {
    name:$source
})

MATCH (b:Entity {
    name:$target
})

MERGE (a)-[
r:RELATION {
    relation:$relation
}
]->(b)
"""

DELETE_DOCUMENT = """
MATCH (d:Document {
    id:$document_id
})

OPTIONAL MATCH (d)-[:HAS_CHUNK]->(c)

DETACH DELETE d,c
"""

GET_CHUNKS_FROM_ENTITY = """
MATCH (e:Entity {
    name:$entity
})

<-[:MENTIONS]-

(c:Chunk)

RETURN
    c.id AS chunk_id,
    c.text AS text,
    c.chunk_index AS chunk_index
"""

GET_NEIGHBOR_ENTITIES = """
MATCH (e:Entity {name:$entity})

-[:RELATION*1..2]-

(n:Entity)

RETURN DISTINCT
n.name AS entity_name,
n.type AS entity_type
"""

SEARCH_ENTITY = """
MATCH (e:Entity)
WHERE toLower(e.name) CONTAINS toLower($name)
RETURN
    e.name AS entity_name,
    e.type AS entity_type
"""

GET_SUBGRAPH = """
MATCH (start:Entity {name:$entity})

OPTIONAL MATCH
path=(start)-[:RELATION*1..3]-(connected:Entity)

WITH
collect(DISTINCT start) +
collect(DISTINCT connected)
AS nodes

UNWIND nodes AS node

RETURN DISTINCT
node.name AS entity_name,
node.type AS entity_type
"""

GET_CONNECTION_PATH = """
MATCH (start:Entity {name:$start})
MATCH (end:Entity {name:$end})

MATCH path = shortestPath(
    (start)-[:RELATION*..10]-(end)
)

RETURN
[pathNode IN nodes(path) | pathNode.name] AS node_names,
[pathRel IN relationships(path) | pathRel.relation] AS relation_names
"""