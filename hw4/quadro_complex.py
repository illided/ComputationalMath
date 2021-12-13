from quadro import *


class QuadroFormulas:
    _possible_forms = {
        'left_rect': left_rectangle,
        'right_rect': right_rectangle,
        'middle_rect': middle_rectangle,
        'trapezoid': trapezoid,
        'simpson': simpson,
        'three_eight': three_eight
    }
    form: Callable[[Callable[[float, float], float], float, float], float]
    function: Callable[[float], float]

    def __init__(self, function: Callable[[float], float], quadro: str = 'simpson'):
        if quadro not in self._possible_forms:
            raise ValueError(f'Form {quadro} does not exist. Possible forms: {self._possible_forms.keys()}')
        self.form = self._possible_forms[quadro]
        self.function = function

    def compute(self, m: int, A: float, B: float) -> float:
        h = (B - A) / m
        result = 0
        for i in range(m):
            result += self.form(self.function, A + i * h, A + (i + 1) * h)
        return result
