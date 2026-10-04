from common.memory import JSONMemory


class EvaluatorMemory(JSONMemory):

    def __init__(self):
        super().__init__(
            "data/evaluator/memory.json"
        )