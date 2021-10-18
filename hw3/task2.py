import numpy as np


class NumericalDifferentiation:
    _X: np.ndarray
    _Y: np.ndarray
    _h: float

    def __init__(self, X, Y):
        self._X = X
        self._Y = Y
        if len(X) < 2 or len(X) != len(Y):
            raise ValueError("Wrong input format")
        self._h = X[1] - X[0]

    def compute(self, first=True, second=True):
        if not first and not second:
            raise ValueError("At least one of the derivative must be picked")
        if len(self._X) == 2 and second:
            raise ValueError("Second derivative can't be calculated with 2 values in table")
        if len(self._X) == 2 and first:
            return np.array([self.left_derivative(), self.right_derivative()]), np.array([np.nan, np.nan])

        answer = []
        if first:
            answer.append(self.first_derivatives())
        if second:
            answer.append(self.second_derivatives())

        return answer

    def left_derivative(self) -> float:
        return (self._Y[1] - self._Y[0]) / self._h

    def right_derivative(self) -> float:
        return self.left_derivative()

    def first_derivatives(self) -> np.ndarray:
        derivatives = []
        start_table_derivative = (-3 * self._Y[0] + 4 * self._Y[1] - self._Y[2]) / (2 * self._h)
        derivatives.append(start_table_derivative)
        for i in range(1, len(self._X) - 1):
            center_derivative = (self._Y[i + 1] - self._Y[i - 1]) / (2 * self._h)
            derivatives.append(center_derivative)
        end = len(self._X) - 1
        end_table_derivatives = (3 * self._Y[end] - 4 * self._Y[end - 1] + self._Y[end - 2]) / (2 * self._h)
        derivatives.append(end_table_derivatives)
        return np.array(derivatives)

    def second_derivatives(self) -> np.ndarray:
        h = self._X[0] - self._X[1]
        derivatives = [np.nan]
        for i in range(1, len(self._X) - 1):
            center_derivative = (self._Y[i + 1] - 2*self._Y[i] + self._Y[i-1]) / (h ** 2)
            derivatives.append(center_derivative)
        derivatives.append(np.nan)
        return np.array(derivatives)