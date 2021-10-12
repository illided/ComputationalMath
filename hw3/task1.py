import numpy as np
from numpy import ndarray
from hw2.launcher import FunctionInterpolation
from hw1.clarification_methods.bisection_method import BisectionMethod
from hw1.segmentation import detekt_root_segments

class SimpleReverseInterpolation(FunctionInterpolation):
    def __init__(self, X, Y):
        super().__init__(Y, X)

    def interpolate(self, y: float, n: int, method='newton', return_used_points=False):
        return super().interpolate(y, n, method, return_used_points)


class RootSearchReverseInterpolation:
    _X: 'ndarray'
    _Y: 'ndarray'

    def __init__(self, X, Y):
        print("Hello")
        self._Y = np.array(Y)
        self._X = np.array(X)

    def interpolate(self, y, n, poly_method: str = 'newton') -> list:
        best_points_indexes = np.argsort(np.abs(self._Y - y))[:n+1]
        X = self._X[best_points_indexes]
        Y = self._Y[best_points_indexes]
        interpolator = FunctionInterpolation(X, Y)
        poly = interpolator.interpolate(X[0], n, method=poly_method)
        segments = detekt_root_segments(np.amin(X), np.amax(X), lambda x: poly(x) - y, 1000, show_segments=False)
        roots = []
        for segment in segments:
            cl_method = BisectionMethod(expr=poly, y=y, print_iterations=False, sym_expr=None)
            roots.append(cl_method.compute(segment))
        return roots
