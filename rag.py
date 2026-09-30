from vectordb.retriever import Retriever
from services.graph_retriever import GraphRetriever
from llm.chat import ChatService
from llm.prompts import RAG_PROMPT


class GraphRAG:

    def __init__(self):

        self.vector = Retriever()

        self.graph = GraphRetriever()

        self.chat = ChatService()

    def build_context(
        self,
        vector_results,
        graph_results,
        graph_paths,
    ):

        context = ""

        # ==========================================================
        # VECTOR RETRIEVAL
        # ==========================================================

        context += "========== VECTOR RETRIEVAL ==========\n\n"

        seen = set()

        for chunk in vector_results:

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            context += chunk["text"] + "\n\n"

        # ==========================================================
        # GRAPH RETRIEVAL
        # ==========================================================

        context += "\n========== GRAPH RETRIEVAL ==========\n\n"

        for chunk in graph_results:

            chunk_id = chunk["chunk_id"]

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            context += chunk["text"] + "\n\n"

        # ==========================================================
        # GRAPH PATHS
        # ==========================================================

        context += "\n========== GRAPH CONNECTION PATHS ==========\n\n"

        if graph_paths:

            for path in graph_paths:

                node_names = path.get("node_names", [])

                relation_names = path.get("relation_names", [])

                if len(node_names) <= 1:
                    continue

                for i in range(len(relation_names)):

                    context += (
                        f"{node_names[i]} "
                        f"--[{relation_names[i]}]--> "
                        f"{node_names[i + 1]}\n"
                    )

                context += "\n"

        else:

            context += "No graph connection found.\n"

        return context

    def ask(self, question):

        # ==========================================
        # Vector Search
        # ==========================================

        vector_results = self.vector.retrieve(question)

        # ==========================================
        # Graph Search
        # ==========================================

        graph_data = self.graph.retrieve(question)

        graph_results = graph_data["chunks"]

        graph_paths = graph_data["paths"]

        # ==========================================
        # Build Prompt Context
        # ==========================================

        context = self.build_context(
            vector_results,
            graph_results,
            graph_paths,
        )

        prompt = RAG_PROMPT.format(
            context=context,
            question=question,
        )
        
        print("=" * 80)
        print("PROMPT CONTEXT")
        print("=" * 80)
        print(context)
        print("=" * 80)

        answer = self.chat.generate(prompt)

        return {

            "answer": answer,

            "vector_sources": vector_results,

            "graph_sources": graph_results,

            "question_entities":
                graph_data["question_entities"],

            "connected_entities":
                graph_data["connected_entities"],

            "paths":
                graph_paths,
        }