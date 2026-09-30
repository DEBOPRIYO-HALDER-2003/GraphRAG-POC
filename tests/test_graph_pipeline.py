from graphdb.graph_extractor import GraphExtractor
from graphdb.neo4j_store import Neo4jStore

text = """
GraphRAG uses Neo4j as a graph database.
GraphRAG uses Qwen for extracting entities.
"""

extractor = GraphExtractor()
neo4j = Neo4jStore()

neo4j.clear_graph()

result = extractor.extract(text)

print(result)

neo4j.save_extraction(result)

print("\nEntities:")
print(neo4j.get_entities())

print("\nRelationships:")
print(neo4j.get_relationships())

neo4j.close()