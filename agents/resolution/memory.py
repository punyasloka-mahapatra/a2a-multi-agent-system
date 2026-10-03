import json
from pathlib import Path


class ResolutionMemory:

    def __init__(self):

        self.file = Path(
            "data/resolution/memory.json"
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
        category,
        resolution
    ):

        data = json.loads(
            self.file.read_text()
        )

        data.append({
            "task_id": task_id,
            "category": category,
            "resolution": resolution
        })

        self.file.write_text(
            json.dumps(
                data,
                indent=2
            )
        )