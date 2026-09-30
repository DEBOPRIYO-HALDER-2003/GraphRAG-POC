import shutil

import streamlit as st

from config import UPLOAD_DIR
from ingest import IngestionPipeline
from rag import GraphRAG


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GraphRAG POC",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def unique_chunks(chunks):
    """
    Remove duplicate chunks using both chunk_id and text.
    """

    unique = []

    seen_ids = set()
    seen_texts = set()

    for chunk in chunks:

        chunk_id = chunk.get("chunk_id")
        text = chunk.get("text", "").strip()

        if chunk_id in seen_ids:
            continue

        if text in seen_texts:
            continue

        seen_ids.add(chunk_id)
        seen_texts.add(text)

        unique.append(chunk)

    return unique


def format_graph_paths(paths):
    """
    Convert graph paths into readable text.
    """

    formatted_paths = []

    for path in paths:

        node_names = path.get(
            "node_names",
            []
        )

        relation_names = path.get(
            "relation_names",
            []
        )

        if len(node_names) < 2:
            continue

        path_text = node_names[0]

        for i, relation in enumerate(relation_names):

            if i + 1 < len(node_names):

                path_text += (
                    f"  └── {relation} → "
                    f"{node_names[i + 1]}"
                )

        formatted_paths.append(path_text)

    return formatted_paths


# ============================================================
# TITLE
# ============================================================

st.title("GraphRAG POC")

st.write(
    "Upload documents, build a knowledge graph and "
    "vector index, then ask questions using hybrid retrieval."
)


# ============================================================
# INITIALIZE GRAPHRAG
# ============================================================

rag = GraphRAG()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Documents")

    uploaded_files = st.file_uploader(
        "Upload Files",
        accept_multiple_files=True,
        type=[
            "pdf",
            "docx",
            "pptx",
            "txt",
            "csv",
            "xlsx"
        ]
    )

    if st.button(
        "🚀 Ingest Documents",
        use_container_width=True
    ):

        if uploaded_files:

            UPLOAD_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            for uploaded_file in uploaded_files:

                destination = (
                    UPLOAD_DIR /
                    uploaded_file.name
                )

                with open(
                    destination,
                    "wb"
                ) as f:

                    shutil.copyfileobj(
                        uploaded_file,
                        f
                    )

            pipeline = IngestionPipeline()

            with st.spinner(
                "Processing documents..."
            ):

                pipeline.run()

            st.success(
                "Documents ingested successfully!"
            )

        else:

            st.warning(
                "Please upload at least one document."
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something about your documents..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.spinner(
        "Searching knowledge graph and vector database..."
    ):

        result = rag.ask(question)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result
        }
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(
                message["content"]
            )

    # --------------------------------------------------------
    # ASSISTANT
    # --------------------------------------------------------

    else:

        with st.chat_message("assistant"):

            result = message["content"]

            # =================================================
            # ANSWER
            # =================================================

            st.markdown("### 🤖 Answer")

            st.write(
                result["answer"]
            )


            # =================================================
            # RETRIEVAL SUMMARY
            # =================================================

            vector_sources = unique_chunks(
                result.get(
                    "vector_sources",
                    []
                )
            )

            graph_sources = unique_chunks(
                result.get(
                    "graph_sources",
                    []
                )
            )

            paths = result.get(
                "paths",
                []
            )

            st.markdown(
                "### 🔎 Retrieval Summary"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Vector Sources",
                    len(vector_sources)
                )

            with col2:

                st.metric(
                    "Graph Sources",
                    len(graph_sources)
                )

            with col3:

                st.metric(
                    "Graph Paths",
                    len(paths)
                )


            # =================================================
            # GRAPH RELATIONSHIPS
            # =================================================

            if paths:

                st.markdown(
                    "### 🧠 Graph Relationships"
                )

                formatted_paths = format_graph_paths(
                    paths
                )

                for path in formatted_paths:

                    st.code(
                        path,
                        language="text"
                    )

            else:

                st.info(
                    "No graph relationships found."
                )


            # =================================================
            # VECTOR SOURCES
            # =================================================

            with st.expander(
                f"🔍 Vector Retrieval "
                f"({len(vector_sources)})"
            ):

                if vector_sources:

                    for i, chunk in enumerate(
                        vector_sources,
                        start=1
                    ):

                        st.markdown(
                            f"**Source {i}**"
                        )

                        st.write(
                            chunk["text"]
                        )

                        st.markdown("---")

                else:

                    st.write(
                        "No vector sources found."
                    )


            # =================================================
            # GRAPH SOURCES
            # =================================================

            with st.expander(
                f"🕸️ Graph Retrieval "
                f"({len(graph_sources)})"
            ):

                if graph_sources:

                    for i, chunk in enumerate(
                        graph_sources,
                        start=1
                    ):

                        st.markdown(
                            f"**Source {i}**"
                        )

                        st.write(
                            chunk["text"]
                        )

                        st.markdown("---")

                else:

                    st.write(
                        "No graph sources found."
                    )


            # =================================================
            # QUESTION ENTITIES
            # =================================================

            question_entities = result.get(
                "question_entities",
                []
            )

            if question_entities:

                with st.expander(
                    "🏷️ Question Entities"
                ):

                    for entity in question_entities:

                        st.markdown(
                            f"- `{entity}`"
                        )


            # =================================================
            # CONNECTED ENTITIES
            # =================================================

            connected_entities = result.get(
                "connected_entities",
                []
            )

            if connected_entities:

                with st.expander(
                    "🔗 Connected Entities"
                ):

                    for entity in connected_entities:

                        st.markdown(
                            f"- `{entity}`"
                        )