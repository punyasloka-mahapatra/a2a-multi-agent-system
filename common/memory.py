import json
from pathlib import Path
from threading import Lock


class JSONMemory:

    def __init__(self, path: str):
        self.file = Path(path)
        self.lock = Lock()

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("[]")

    def save(self, record: dict):

        with self.lock:

            try:
                data = json.loads(
                    self.file.read_text()
                )
            except json.JSONDecodeError:
                data = []

            data.append(record)

            self.file.write_text(
                json.dumps(
                    data,
                    indent=2
                )
            )