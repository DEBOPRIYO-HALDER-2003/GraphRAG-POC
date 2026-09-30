import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag import RAGPipeline


def main():

    rag = RAGPipeline()

    while True:

        print()

        question = input("Ask : ")

        if question.lower() == "exit":
            break

        response = rag.ask(question)

        print("\n" + "="*80)

        print("\nAnswer\n")

        print(response["answer"])

        print("\nRetrieved Sources\n")

        for i, source in enumerate(response["sources"], start=1):

            print(f"Source {i}")

            print(source["text"][:300])

            print("-"*80)


if __name__ == "__main__":
    main()