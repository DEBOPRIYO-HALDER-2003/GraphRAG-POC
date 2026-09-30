import json

from config import REGISTRY_FILE


class IngestionRegistry:

    def __init__(self):

        REGISTRY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not REGISTRY_FILE.exists():

            with open(REGISTRY_FILE, "w") as f:

                json.dump({}, f, indent=4)

        self.registry = self.load()

    def load(self):

        with open(REGISTRY_FILE, "r") as f:

            return json.load(f)

    def save(self):

        with open(REGISTRY_FILE, "w") as f:

            json.dump(
                self.registry,
                f,
                indent=4
            )

    def is_ingested(
        self,
        filename,
        file_hash
    ):

        if filename not in self.registry:

            return False

        return (
            self.registry[filename]["hash"]
            == file_hash
        )

    def add_document(
        self,
        filename,
        file_hash
    ):

        self.registry[filename] = {
            "hash": file_hash
        }

        self.save()

    def remove_document(
        self,
        filename
    ):

        if filename in self.registry:

            del self.registry[filename]

            self.save()

    def get_documents(self):

        return list(
            self.registry.keys()
        )