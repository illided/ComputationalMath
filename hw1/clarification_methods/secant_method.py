from abc import ABC

from .clarification_methods import ClarificationMethod


class SecantMethod(ClarificationMethod, ABC):
    x0: float
    x1: float

    def get_error(self):
        return self.get_clarification()

    def compute(self, segment) -> float:
        self.x0 = segment[0]
        self.x1 = segment[1]
        return super().compute(segment)

    def clarify_once(self):
        x0 = self.x0
        x1 = self.x1
        f = self.expr

        self.current_x = x1 - ((x1 - x0) * f(x1)) / (f(x1) - f(x0))

        self.x0 = x1
        self.x1 = self.current_x
