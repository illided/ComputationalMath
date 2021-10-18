import numpy as np
import pandas as pd
import streamlit as st
import sympy
import matplotlib.pyplot as plt
from hw2.layout import get_region, get_table_size, get_interpolation_parameters, represents_int, represents_float
from task1 import SimpleReverseInterpolation, RootSearchReverseInterpolation
from hw2.launcher import create_table

from task2 import NumericalDifferentiation


def task_3_1():
    function = 'exp(x) + sin(x)'
    function_as_lambda = sympy.lambdify('x', sympy.parse_expr(function))

    a, b = get_region()
    t_s = get_table_size()
    y, n = get_interpolation_parameters(t_s, variable='y')

    X_t, Y_t = create_table(t_s, (a, b), function)
    st.write(pd.DataFrame([X_t, Y_t], index=['x', 'f(x)']))

    X = np.linspace(a, b)
    Y_target = np.full_like(X, y)
    Y_function = [function_as_lambda(x) for x in X]
    col1, col2 = st.columns(2)

    def plot_prediction(predictions: list, column):
        Y_p = [function_as_lambda(pr) for pr in predictions]
        fig, ax = plt.subplots()
        ax.plot(X, Y_target, "--")
        ax.plot(X, Y_function)
        ax.plot(predictions, Y_p, 'ro')
        column.pyplot(fig)

    col1.write('Отражение таблицы')
    col2.write('Интерполирование и поиск корней')

    sr = SimpleReverseInterpolation(X_t, Y_t)
    sr_pred = [sr.interpolate(y, n)(y)]

    plot_prediction(sr_pred, col1)
    col1.write(f'Ошибка: {abs(function_as_lambda(sr_pred[0]) - y)}')

    rs = RootSearchReverseInterpolation(X_t, Y_t)
    rs_pred = rs.interpolate(y, n)

    plot_prediction(rs_pred, col2)
    errors = [abs(function_as_lambda(pr) - y) for pr in rs_pred]
    col2.write(f'Ошибки: {errors}')
    col2.write(f'Средняя ошибка: {np.mean(np.array(errors))}')


def task3_2():
    function = 'exp(7*x)'
    function_se = sympy.parse_expr(function)
    fd_se = sympy.diff(function_se, "x")
    sd_se = sympy.diff(function_se, ("x", 2))
    first_der = sympy.lambdify("x", fd_se)
    second_der = sympy.lambdify("x", sd_se)
    st.write(f"Рассматриваемая функция: {function}")
    with st.form("Параметры задачи:"):
        a = st.text_input("Введите a - начало промежутка")
        h = st.text_input("Введите h - расстояние между точками")
        m = st.text_input("Введите m - количество точек")
        submit = st.form_submit_button("Решить задачу")
        if not submit:
            st.stop()
        if not (represents_int(m) and represents_float(a) and represents_float(h)):
            st.error("Неправильный формат введеных данных")
            st.stop()
    a, h, m = float(a), float(h), int(m)
    X, Y = create_table(m + 1, (a, a + h * m), function)
    ND = NumericalDifferentiation(X, Y)
    predicted_fd, predicted_sd = ND.compute()
    fd_error = np.abs(first_der(X) - predicted_fd)
    sd_error = np.abs(second_der(X) - predicted_sd)
    st.dataframe(pd.DataFrame([X, Y, predicted_fd, fd_error, predicted_sd, sd_error],
                              index=["x", "f(x)", "f'(x)", "f'(x) error", "f''(x)", "f''(x) error"]).T)


def main():
    st.header("Лабораторная работа №3")
    task = st.sidebar.selectbox("Выберите подзадачу",
                                ["1. Обратное интерполирование",
                                 "2. Нахождение производных по формулам численного дифференцирования"])
    if task == '1. Обратное интерполирование':
        task_3_1()
    elif task == '2. Нахождение производных по формулам численного дифференцирования':
        task3_2()


if __name__ == '__main__':
    main()
