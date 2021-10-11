import numpy as np

from launcher import FunctionInterpolation, create_table
import pandas as pd
import matplotlib.pyplot as plt
import sympy
from layout import get_region, get_interpolation_parameters, represents_int
import streamlit as st

variant = 9
function = "1 - exp(-x) + x**2"
function_as_lambda = sympy.lambdify('x', sympy.parse_expr(function))

st.set_page_config(layout="wide")

st.header("Задача алгебраического интерполирования")
st.subheader(f"Вариант №{variant}")
st.write(f'Интерполируемая функция: f(x) = {function}')

a, b = get_region()

st.write(f'Границы интерполирования: [{a}, {b}]')

t_s = st.text_input(label="Введите число значений в таблице")
if not t_s:
    st.stop()
if not represents_int(t_s):
    st.warning("Неправильный формат числа")
    st.stop()
interpolator = FunctionInterpolation(*create_table(int(t_s), (a, b), function))

st.write("Исходная таблица значений функции")
st.write(pd.DataFrame(interpolator.table, index=["x", "f(x)"]))

x, n = get_interpolation_parameters()

n_poly, X_used, Y_used = interpolator.interpolate(x, n, method='newton', return_used_points=True)
l_poly = interpolator.interpolate(x, n, method='lagrange')

st.write("Использующиеся точки:")
st.write(pd.DataFrame([X_used, Y_used], index=["x", "f(x)"]))

st.write("Полученное интерполирование:")

col1, col2 = st.columns(2)


def plot_prediction(poly, col):
    y = poly(x)
    y_actual = function_as_lambda(x)

    col.write(f"P(x) = {y}")
    col.write(f'Абсолютная погрешность: {abs(y - y_actual)}')

    X = np.linspace(x - abs(X_used[-1] - x) - 1, x + abs(X_used[-1] - x) + 2)
    Y_actual = np.array([function_as_lambda(p) for p in X])
    Y_predicted = np.array([poly(p) for p in X])

    fig, ax = plt.subplots()
    ax.plot(X, Y_actual, label="f(x)")
    ax.plot(X, Y_predicted, "m", label="P(x)")
    ax.plot(X_used, Y_used, 'bo', label="Точки интерполирования")
    ax.plot(x, y, 'ro', label="x")
    ax.legend(loc="lower right")
    col.pyplot(fig)


col1.write("Метод Ньютона")
plot_prediction(n_poly, col1)

col2.write("Метод Лагранжа")
plot_prediction(l_poly, col2)
