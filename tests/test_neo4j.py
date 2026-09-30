from graphdb.neo4j_store import Neo4jStore


db = Neo4jStore()

print("\nTesting connection...")

print(db.test_connection())

print("\nClearing graph...")

db.clear_graph()

print("\nAdding entities...")

db.create_entity("Neo4j", "Database")
db.create_entity("GraphRAG", "Framework")
db.create_entity("Qwen", "LLM")

print("\nAdding relationships...")

db.create_relationship(
    "GraphRAG",
    "USES",
    "Neo4j"
)

db.create_relationship(
    "GraphRAG",
    "USES",
    "Qwen"
)

print("\nEntities")

print(db.get_entities())

print("\nRelationships")

print(db.get_relationships())

db.close()