from abc import ABC

from sympy import lambdify, diff

from clarification_methods.clarification_methods import ClarificationMethod


class ModifiedNewtonMethod(ClarificationMethod, ABC):
    df_in_start: float

    def get_error(self):
        return self.get_clarification()

    def compute(self, segment) -> float:
        df = lambdify(self.variable, diff(self.sym_expr))
        self.df_in_start = df(segment[0])
        return super().compute(segment)

    def clarify_once(self):
        self.current_x = self.current_x - self.expr(self.current_x) / self.df_in_start
