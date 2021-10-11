from numpy import ndarray
from typing import Callable
from hw2.launcher import FunctionInterpolation
from hw1.clarification_methods.bisection_method import BisectionMethod


def detekt_root_segments(A, B, F: Callable, N, show_segments: bool = True) -> list:
    h = (B - A) / N
    position = A
    previous_calculation = F(A)
    root_segments = []
    while position < B:
        position += h
        new_calculation = F(position)
        if previous_calculation * new_calculation <= 0:
            segment = [position - h, position]
            root_segments.append(segment)
            if show_segments:
                print(f'Found segment: {segment}')
        previous_calculation = new_calculation
    return root_segments

class SimpleReverseInterpolation(FunctionInterpolation):
    def __init__(self, X, Y):
        super().__init__(Y, X)

    def interpolate(self, y: float, n: int, method='newton', return_used_points=False):
        return super().interpolate(y, n, method, return_used_points)


class RootSearchReverseInterpolation:
    _X: 'ndarray'
    _Y: 'ndarray'

    def __init__(self, X, Y):
        self._Y = Y
        self._X = X

    def interpolate(self, y, poly_method: str = 'newton') -> list:
        interpolator = FunctionInterpolation(self._X, self._Y)
        poly = interpolator.interpolate(self._X[0], self._X.shape[0], method=poly_method)
        segments = detekt_root_segments(self._X[0], self._X[-1], lambda x: poly(x) - y, 1000, show_segments=True)
        roots = []
        for segment in segments:
            cl_method = BisectionMethod(expr=poly, y=y, print_iterations=True, sym_expr=None)
            roots.append(cl_method.compute(segment))
        return roots
