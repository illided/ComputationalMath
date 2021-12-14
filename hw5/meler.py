from math import cos, pi, sqrt
from typing import Callable, List


def get_Meler_points(n: int) -> List[float]:
    return [cos(((2*k-1) * pi) / (2 * n)) for k in range(1, n + 1)]


def get_Meler_coef(n: int) -> List[float]:
    return [pi / n for _ in range(n)]


def weight(x):
    return 1 / sqrt(1 - x ** 2)


def integrate(f: Callable[[float], float], n: int = 5) -> float:
    points = get_Meler_points(n)
    coef = get_Meler_coef(n)
    return sum([c * f(x) for c, x in zip(coef, points)])
