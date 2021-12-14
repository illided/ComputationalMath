import streamlit as st
from sympy import lambdify, parse_expr
from gauss import GaussQuadro
import meler
import pandas as pd

import scipy.integrate as integrate


def Gauss():
    st.header("КФ Гаусса, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Гаусса.")

    with st.form("Введите параметры задачи"):
        f_string = st.text_input("f(x) - функция, для которой считается интеграл")
        col1, col2 = st.columns(2)
        a = col1.text_input("a - левая граница")
        b = col2.text_input("b - левая граница")
        N_string = st.text_input("Количество узлов для сравнения (через запятую)")

        with st.expander("Дополнительные параметры"):
            splits = int(float(st.text_input("Количество разбиений отрезка", value="1e6")))
            eps = float(st.text_input("Точность нахождения корней", value="1e-12"))
            percent_err_prec = int(st.text_input("Количество знаков после запятой у PercentError", value="4"))

        if st.form_submit_button("Решить задачу"):
            a = get_float(a)
            b = get_float(b)
            if b < a:
                st.error("Левая граница должна быть меньше правой")
            f = lambdify("x", parse_expr(f_string))
        else:
            st.stop()
        N_list = [int(n) for n in N_string.split(",")]

    real_value = integrate.quad(f, a, b)[0]

    st.latex(fr"\int_{{{a}}}^{{{b}}} {f_string} = J = {real_value}")

    def print_for_N(N: int):
        st.subheader(f"N = {N}")
        formula = GaussQuadro(a, b, N, number_of_segments=splits, clarification_precision=eps)

        KF = pd.DataFrame([formula.g_points, formula.g_coef])
        KF.index = ["x_i", "A_i"]
        st.dataframe(KF)

        result = formula.compute(f)
        st.latex(fr'J_{{{N}}} = {result}')
        err = abs(result - real_value)
        st.latex(fr'|J - J_{{{N}}}| = {err}')
        st.latex(fr'PercentError \approx {round(abs(err / real_value) * 100, percent_err_prec)} \%')

    for N in N_list:
        print_for_N(N)


def Meler():
    st.header("КФ Мелера, ее узлы и коэффициенты. Вычисление интегралов при помощи КФ Мелера.")

    with st.form("Введите данные задачи."):
        f_string = st.text_input("f(x) - функция, для которой считается интеграл")
        N_string = st.text_input("Количество узлов для сравнения (через запятую)")

        with st.expander("Дополнительные параметры"):
            percent_err_prec = int(st.text_input("Количество знаков после запятой у PercentError", value="4"))

        if st.form_submit_button("Решить задачу"):
            f = lambdify('x', parse_expr(f_string))
            N_list = [int(n) for n in N_string.split(",")]
        else:
            st.stop()

    F = lambda x: meler.weight(x) * f(x)
    real_value = integrate.quad(F, -1, 1)[0]
    st.latex(fr"\int_{{-1}}^{{1}} p(x) * {f_string} = J = {real_value}")

    def print_for_N(N: int):
        st.subheader(f"N = {N}")
        points = meler.get_Meler_points(N)
        coef = meler.get_Meler_coef(N)

        KF = pd.DataFrame([points, coef])
        KF.index = ["x_i", "A_i"]
        st.dataframe(KF)

        result = meler.integrate(f, N)
        st.latex(fr'J_{{{N}}} = {result}')
        err = abs(result - real_value)
        st.latex(fr'|J - J_{{{N}}}| = {err}')
        st.latex(fr'PercentError \approx {round(abs(err / real_value) * 100, percent_err_prec)} \%')

    for N in N_list:
        print_for_N(N)


def get_float(s):
    try:
        return float(s)
    except TypeError:
        st.error(f"Ожидалось число с плавающей запятой, но было получено {s}")


possible_methods = ["КФ Гаусса", "КФ Мелера"]
method = st.sidebar.selectbox(label="Выберите подзадачу", options=possible_methods)

if method == "КФ Гаусса":
    Gauss()
elif method == "КФ Мелера":
    Meler()
