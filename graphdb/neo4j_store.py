from neo4j import GraphDatabase

from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
)

from graphdb.cypher_queries import (
    CREATE_DOCUMENT,
    CREATE_CHUNK,
    LINK_DOCUMENT_CHUNK,
    CREATE_ENTITY,
    LINK_CHUNK_ENTITY,
    CREATE_RELATIONSHIP,
    GET_CHUNKS_FROM_ENTITY,
    GET_NEIGHBOR_ENTITIES,
    SEARCH_ENTITY,
    GET_SUBGRAPH,
    GET_CONNECTION_PATH
)

from utils.logger import logger


class Neo4jStore:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

        logger.info("Connected to Neo4j.")

    def close(self):

        self.driver.close()

    def create_entity(self, name: str, entity_type: str):

        with self.driver.session() as session:

            session.run(
                CREATE_ENTITY,
                name=name,
                type=entity_type
            )

    def create_relationship(
        self,
        source: str,
        relation: str,
        target: str,
    ):

        with self.driver.session() as session:

            session.run(
                CREATE_RELATIONSHIP,
                source=source,
                relation=relation,
                target=target,
            )

    def create_document(
        self,
        document_id,
        filename,
    ):

        with self.driver.session() as session:

            session.run(
                CREATE_DOCUMENT,
                document_id=document_id,
                filename=filename,
            )
            
    def create_chunk(
        self,
        chunk_id,
        text,
        chunk_index,
    ):

        with self.driver.session() as session:

            session.run(
                CREATE_CHUNK,
                chunk_id=chunk_id,
                text=text,
                chunk_index=chunk_index,
            )

    def link_document_chunk(
        self,
        document_id,
        chunk_id,
    ):

        with self.driver.session() as session:

            session.run(
                LINK_DOCUMENT_CHUNK,
                document_id=document_id,
                chunk_id=chunk_id,
            )
            
    def link_chunk_entity(
        self,
        chunk_id,
        entity_name,
    ):

        with self.driver.session() as session:

            session.run(
                LINK_CHUNK_ENTITY,
                chunk_id=chunk_id,
                entity_name=entity_name,
            )
            
    def get_chunks_from_entity(
    self,
    entity,
    ):

        with self.driver.session() as session:

            result = session.run(
                GET_CHUNKS_FROM_ENTITY,
                entity=entity,
            )

            return [
                record.data()
                for record in result
            ]
            
    def get_neighbor_entities(
        self,
        entity,
    ):

        with self.driver.session() as session:

            result = session.run(
                GET_NEIGHBOR_ENTITIES,
                entity=entity,
            )

            return [
                record.data()
                for record in result
            ]

    def search_entity(self, name: str):

        with self.driver.session() as session:

            result = session.run(
                SEARCH_ENTITY,
                name=name
            )

            return [record.data() for record in result]


    def test_connection(self):

        try:

            with self.driver.session() as session:

                session.run("RETURN 1")

            logger.info("Neo4j connection successful.")

            return True

        except Exception as e:

            logger.exception(e)

            return False
        
    def get_subgraph(
    self,
    entity,
    ):

        with self.driver.session() as session:

            result = session.run(
                GET_SUBGRAPH,
                entity=entity,
            )

            return [
                record.data()
                for record in result
            ]
    
    def get_connection_path(
        self,
        start,
        end,
    ):

        with self.driver.session() as session:

            result = session.run(
                GET_CONNECTION_PATH,
                start=start,
                end=end,
            )

            record = result.single()

            if record is None:
                return None

            return record.data()
        
        
    def save_extraction(

        self,

        document_id,

        filename,

        chunk_id,

        chunk_text,

        chunk_index,

        extraction,

    ):

        self.create_document(
            document_id,
            filename,
        )

        self.create_chunk(
            chunk_id,
            chunk_text,
            chunk_index,
        )

        self.link_document_chunk(
            document_id,
            chunk_id,
        )

        entities = extraction.get(
            "entities",
            [],
        )

        relationships = extraction.get(
            "relationships",
            [],
        )

        for entity in entities:

            self.create_entity(
                entity["name"],
                entity["type"],
            )

            self.link_chunk_entity(
                chunk_id,
                entity["name"],
            )

        for relation in relationships:

            self.create_relationship(
                relation["source"],
                relation["relation"],
                relation["target"],
            )