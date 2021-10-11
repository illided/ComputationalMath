import numpy as np
from numpy import ndarray
import sympy
from typing import Any, Callable, Optional, Tuple
from .newton_poly import newton_poly
from .lagrange_poly import lagrange_poly


def create_table(table_size: int, region: tuple, table_function: str, variable='x'):
    table_function_as_lambda = sympy.lambdify(variable, sympy.parse_expr(table_function))
    a, b = region
    x = np.linspace(a, b, table_size)
    return x, [table_function_as_lambda(p) for p in x]


class FunctionInterpolation:
    table: 'ndarray'
    _possible_interpolation_methods = {'newton': newton_poly, 'lagrange': lagrange_poly}

    def __init__(self, X, Y):
        self.table = np.array([X, Y])

    def _get_closest_point_indexes(self, x, n) -> ndarray:
        return self.table[:, np.argsort(np.abs(self.table[0, :] - x))][:, :n]

    def interpolate(self, x: float, n: int, method='newton', return_used_points=False):
        method_as_lambda = self._possible_interpolation_methods[method]
        X, Y = self._get_closest_point_indexes(x, n + 1)
        poly = method_as_lambda(X, Y)
        if return_used_points:
            return poly, X, Y
        return poly
