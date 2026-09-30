import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from llm.chat import ChatService


def main():

    chat = ChatService()

    answer = chat.generate(
        "Explain what is Artificial Intelligence in two lines."
    )

    print()

    print(answer)


if __name__ == "__main__":
    main()