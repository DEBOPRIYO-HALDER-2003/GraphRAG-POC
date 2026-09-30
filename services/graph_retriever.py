from graphdb.graph_extractor import GraphExtractor
from graphdb.neo4j_store import Neo4jStore


class GraphRetriever:

    def __init__(self):

        self.neo4j = Neo4jStore()
        self.extractor = GraphExtractor()

    def extract_question_entities(self, question):

        extraction = self.extractor.extract(question)

        entities = extraction.get("entities", [])

        normalized = []

        for entity in entities:

            matches = self.neo4j.search_entity(entity["name"])

            if matches:

                normalized.append(matches[0]["entity_name"])

        return normalized

    def find_connection_paths(
        self,
        question_entities,
    ):

        if len(question_entities) < 2:
            return []

        paths = []

        for i in range(len(question_entities)):

            for j in range(i + 1, len(question_entities)):

                path = self.neo4j.get_connection_path(
                    question_entities[i],
                    question_entities[j],
                )

                if path:

                    paths.append(path)

        return paths
    
    def extract_entities_from_paths(
        self,
        paths,
    ):

        entities = set()

        for path in paths:

            for entity_name in path["node_names"]:

                entities.add(entity_name)

        return list(entities)

    def collect_chunks(self, entities):

        chunks = []
        seen = set()

        for entity in entities:

            results = self.neo4j.get_chunks_from_entity(entity)

            for chunk in results:

                chunk_id = chunk["chunk_id"]

                if chunk_id in seen:
                    continue

                seen.add(chunk_id)
                chunks.append(chunk)

        return chunks

    def retrieve(self, question):

        question_entities = self.extract_question_entities(question)

        if not question_entities:
            return {
                "question_entities": [],
                "connected_entities": [],
                "paths": [],
                "chunks": [],
            }

        paths = self.find_connection_paths(
            question_entities
        )
        
        print("=" * 80)
        print(paths)
        print("=" * 80)

        connected_entities = self.extract_entities_from_paths(
            paths
        )

        graph_chunks = self.collect_chunks(
            connected_entities
        )

        # ================= DEBUG =================

        print("=" * 80)
        print("QUESTION ENTITIES")
        print(question_entities)

        print("=" * 80)
        print("PATHS")
        print(paths)

        print("=" * 80)
        print("CONNECTED ENTITIES")
        print(connected_entities)

        print("=" * 80)
        print("GRAPH CHUNKS")
        print(graph_chunks)

        print("=" * 80)

        # =========================================

        return {
            "question_entities": question_entities,
            "connected_entities": connected_entities,
            "paths": paths,
            "chunks": graph_chunks,
        }