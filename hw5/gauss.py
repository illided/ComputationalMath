from typing import Callable, List
from math import factorial
import numpy as np
from hw1.segmentation import detekt_root_segments
from hw1.clarification_methods.secant_method import SecantMethod


def generalized_binomial(n: float, k: int):
    numerator = np.prod([n - i for i in range(k)])
    denominator = factorial(k)
    return numerator / denominator


def sum_poly(polys: List[Callable[[float], float]]) -> Callable[[float], float]:
    def poly(x) -> float:
        return sum([p(x) for p in polys])

    return poly


def monom(c, n):
    return lambda x: c * (x ** n)


def construct_poly(coef: List[float]) -> Callable[[float], float]:
    polys = []
    for i, c in enumerate(coef):
        polys.append(monom(c, i))
    return sum_poly(polys)


def get_Legendre_coef(degree: int) -> List[float]:
    coef = []
    for k in range(degree + 1):
        coef.append(generalized_binomial(degree, k) * generalized_binomial((degree + k - 1) / 2, degree))
    return [2 ** degree * c for c in coef]


class GaussQuadro:
    def __init__(self, a, b, N: int = 5, number_of_segments=10 ** 7, clarification_precision=10 ** (-12)):
        self.a = a
        self.b = b
        self.N = N
        self.number_of_segments = number_of_segments
        self.clarification_precision = clarification_precision

        self.legendre_coef = get_Legendre_coef(N)
        self.legendre_poly = construct_poly(self.legendre_coef)

        self.g_points = None
        self.compute_Gauss_points()

        self.g_coef = None
        self.compute_Gauss_coef()

        self.scale()

    def compute_Gauss_points(self):
        root_segments = detekt_root_segments(-1, 1, self.legendre_poly, self.number_of_segments, show_segments=False)
        method = SecantMethod(sym_expr=None, expr=self.legendre_poly, print_iterations=False,
                              e=self.clarification_precision)
        self.g_points = [method.compute(s) for s in root_segments]

    def compute_Gauss_coef(self):
        p_n_1 = construct_poly(get_Legendre_coef(self.N - 1))
        self.g_coef = []
        for x in self.g_points:
            new_coef = 2 * (1 - x ** 2) / (self.N ** 2 * p_n_1(x) ** 2)
            self.g_coef.append(new_coef)

    def scale(self):
        q = (self.b - self.a) / 2
        self.g_points = [self.a + q * (x + 1) for x in self.g_points]
        self.g_coef = [q * A for A in self.g_coef]

    def compute(self, f: Callable[[float], float]):
        return sum([c * f(x) for c, x in zip(self.g_coef, self.g_points)])

