import json
from pathlib import Path


class ResponseMemory:

    def __init__(self):

        self.file = Path(
            "data/response/memory.json"
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
        response
    ):

        data = json.loads(
            self.file.read_text()
        )

        data.append({
            "task_id": task_id,
            "response": response
        })

        self.file.write_text(
            json.dumps(
                data,
                indent=2
            )
        )