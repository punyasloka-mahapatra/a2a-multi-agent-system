import json
from pathlib import Path


class ClassifierMemory:

    def __init__(self):

        self.file = Path(
            "data/classifier/memory.json"
        )

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("[]")

    def save(
        self,
        task_id,
        customer_message,
        category
    ):

        data = json.loads(
            self.file.read_text()
        )

        data.append({
            "task_id": task_id,
            "customer_message": customer_message,
            "category": category
        })

        self.file.write_text(
            json.dumps(
                data,
                indent=2
            )
        )