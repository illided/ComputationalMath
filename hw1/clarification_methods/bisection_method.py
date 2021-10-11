from abc import ABC

from clarification_methods.clarification_methods import ClarificationMethod


class BisectionMethod(ClarificationMethod, ABC):
    def get_error(self):
        return 2 * abs(self.segment[1] - self.segment[0])

    def clarify_once(self):
        a = self.segment[0]
        b = self.segment[1]
        middle = a + (b - a) / 2
        if self.expr(a) * self.expr(middle) <= 0:
            self.segment = [a, middle]
        else:
            self.segment = [middle, b]
        self.current_x = middle
