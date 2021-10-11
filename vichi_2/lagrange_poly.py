from typing import List, Callable
import numpy as np


def lagrange_poly(X, Y):
    polys = []
    for i in range(len(X)):
        polys.append(get_poly(X, i, Y[i]))
    return get_sum_of_poly(polys)


def get_sum_of_poly(polys: List[Callable]) -> Callable:
    def poly_sum(x):
        y = 0
        for poly in polys:
            y += poly(x)
        return y

    return poly_sum


def get_poly(X, index, coef):
    except_index = np.concatenate([X[0:index], X[index + 1:]])
    denominator = np.prod(X[index] - except_index)

    def poly(x):
        numerator = coef * np.prod(x - except_index)
        return numerator / denominator

    return poly
