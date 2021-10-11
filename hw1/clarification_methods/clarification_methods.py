from typing import Any, Callable

from sympy import lambdify


class ClarificationMethod:
    sym_expr: Any
    target: float
    expr: Callable
    max_iteration: int
    variable: str
    e: float
    is_responsive: bool
    current_x: float
    last_x: float
    iterations_passed: int
    segment: list
    finished: bool

    def __init__(self, sym_expr, y: float = 0, max_iteration: int = 10,
                 variable: str = 'x', e: float = 10 ** (-6),
                 print_iterations: bool = True):
        self.sym_expr = sym_expr
        self.target = y
        self.expr = lambdify(variable, sym_expr)
        self.max_iteration = max_iteration
        self.variable = variable
        self.e = e
        self.is_responsive = print_iterations
        self.current_x = None
        self.last_x = None
        self.iterations_passed = 0
        self.finished = False

    def get_error(self):
        return abs(self.expr(self.current_x) - self.target)

    def get_clarification(self):
        return abs(self.current_x - self.last_x)

    def print_stat(self):
        print(f'Iteration {self.iterations_passed}, x={self.current_x}, '
              f'error={self.get_error()}, clarification: {abs(self.current_x - self.last_x)}')

    def clarify_once(self):
        raise NotImplementedError()

    def compute(self, segment) -> float:
        self.iterations_passed = 0
        self.segment = segment
        self.current_x = segment[0]
        self.last_x = segment[1]
        while self.get_error() > self.e:
            if self.iterations_passed >= self.max_iteration:
                self.finished = False
                return self.current_x
            self.last_x = self.current_x
            self.clarify_once()
            self.iterations_passed += 1
            if self.is_responsive:
                self.print_stat()
        self.finished = True
        return self.current_x
