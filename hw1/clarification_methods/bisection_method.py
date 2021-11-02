from abc import ABC

from .clarification_methods import ClarificationMethod


class BisectionMethod(ClarificationMethod, ABC):
    def get_error(self):
        return 2 * abs(self.segment[1] - self.segment[0])

    def clarify_once(self):
        a = self.segment[0]
        b = self.segment[1]
        middle = a + (b - a) / 2
        f_a = self.expr(a) - self.target
        f_b = self.expr(b) - self.target
        f_m = self.expr(middle) - self.target
        if f_m == 0:
            self.current_x = middle
            return
        if f_a == 0:
            self.current_x = a
        if f_b == 0:
            self.current_x = b
        if f_a * f_m < 0:
            self.segment = [a, middle]
        elif f_b * f_m < 0:
            self.segment = [middle, b]
        else:
            raise ValueError("Segmentation error")
        self.current_x = middle
