from typing import Callable


def left_rectangle(f: Callable, a: float, b: float) -> float:
    return (b - a) * f(a)


def right_rectangle(f: Callable, a: float, b: float) -> float:
    return (b - a) * f(b)


def middle_rectangle(f: Callable, a: float, b: float) -> float:
    return (b - a) * f((a + b) / 2)


def trapezoid(f: Callable, a: float, b: float) -> float:
    return (b - a) / 2 * (f(a) + f(b))


def simpson(f: Callable, a: float, b: float) -> float:
    return ((b - a) / 6) * (f(a) + 4 * f((a + b) / 2) + f(b))


def three_eight(f: Callable, a: float, b: float) -> float:
    h = (b - a) / 3
    return (b - a) * (1/8 * f(a) + 3/8 * f(a + h) + 3/8 * f(a + 2 * h) + 1/8 * f(b))


