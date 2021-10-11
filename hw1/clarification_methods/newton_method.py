from typing import Any

from sympy import lambdify, diff

from clarification_methods.clarification_methods import ClarificationMethod


class NewtonMethod(ClarificationMethod):
    df: Any

    def get_error(self):
        return self.get_clarification()

    def __init__(self, sym_expr, **kwargs):
        super().__init__(sym_expr, **kwargs)
        self.df = lambdify(self.variable, diff(sym_expr))

    def clarify_once(self):
        self.current_x = self.current_x - self.expr(self.current_x) / self.df(self.current_x)
