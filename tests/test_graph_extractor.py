from graphdb.graph_extractor import GraphExtractor

extractor = GraphExtractor()

text = """
GraphRAG uses Neo4j as a graph database.
GraphRAG also uses Qwen for entity extraction.
"""

result = extractor.extract(text)

print(result)