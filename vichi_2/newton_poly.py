from typing import Callable, List
import numpy as np


def sub_poly(substractors, coef: float) -> Callable:
    def poly(x):
        return coef * np.prod(x - substractors)

    return poly


def get_sum_of_poly(polys: List[Callable]) -> Callable:
    def poly_sum(x):
        y = 0
        for poly in polys:
            y += poly(x)
        return y

    return poly_sum


def divided_difference(X, Y):
    n = X.shape[0]
    coef = np.zeros((n, n))
    coef[:, 0] = Y

    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (X[i + j] - X[i])

    return coef


def newton_poly(X, Y):
    coef = divided_difference(X, Y)
    polys = [lambda x: Y[0]]
    n = len(X) - 1
    for i in range(n):
        polys.append(sub_poly(X[0 :i + 1], coef[0, i + 1]))
    return get_sum_of_poly(polys)