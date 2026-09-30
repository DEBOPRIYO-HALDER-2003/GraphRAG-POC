from rag import GraphRAG

rag = GraphRAG()

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":

        break

    result = rag.ask(question)

    print("\nAnswer:\n")

    print(result["answer"])

    print("\nRetrieved Chunks:\n")

    for chunk in result["sources"]:

        print("-" * 60)

        print(chunk["text"])

    print("\nEntities:\n")

    for entity in result["entities"]:

        print(entity)

    print("\nRelationships:\n")

    for relation in result["relationships"]:

        print(relation)