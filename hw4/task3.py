import streamlit as st
from sympy import lambdify, parse_expr, diff
from quadro_complex import *
import scipy.integrate as integrate

st.header("Лабораторная работа #4.3")


def get_float(s):
    try:
        return float(s)
    except TypeError:
        st.error(f"Ожидалось число с плавающей запятой, но было получено {s}")


def get_int(s):
    try:
        return int(s)
    except TypeError:
        st.error(f'Ожидалось целое число но было получено: {s}')


with st.form("Введите параметры задачи"):
    f_string = st.text_input("f - функция, для которой считается интеграл")
    col1, col2 = st.columns(2)
    a = col1.text_input("a - левая граница")
    b = col2.text_input("b - правая граница")
    m = st.text_input('m - количество разбиений')
    l = st.text_input('l - увеличение разбиений')
    if st.form_submit_button("Решить задачу"):
        a = get_float(a)
        b = get_float(b)
        l = get_int(l)
        if b < a:
            st.error("Левая граница должна быть меньше правой")
        m = get_int(m)
        if m < 1:
            st.error("Количество разбиений должно быть больше одного")
        f = lambdify("x", parse_expr(f_string))
    else:
        st.stop()

st.subheader("Реальное значение")

try:
    real_value = integrate.quad(f, a, b)[0]
except ZeroDivisionError:
    st.error("Функция не интегрируема на данном промежутке")
    st.stop()
st.latex(fr'\int_{{{a}}}^{{{b}}} {f_string} = J = {real_value}')


def print_abs_fact_error(real, var, col):
    err = abs(real_value - real)
    col.latex(f"|{var} - J| = {err}")


def print_relative_abs_error(real, col):
    err = abs(real_value - real)
    col.latex(fr'PercentError = {round(abs(err / real_value) * 100, 4)} \%')


def print_runge(j_h, j_hl, d, col):
    r = d + 1
    J_better = ((l ** r) * j_hl - j_h) / (l ** r - 1)
    col.latex(fr'\overline{{J}} = {J_better}')
    return J_better


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def print_method(method_name_russian, method_name, AST):
    st.subheader(method_name_russian)
    col1, col2, col3 = st.columns(3)
    form = QuadroFormulas(f, method_name)
    J_h = form.compute(m, a, b)
    camel_case = to_camel_case(method_name)
    col1.latex(fr'J_{{{camel_case}}}(h) = {J_h}')
    J_hl = form.compute(m * l, a, b)
    col1.latex(fr'J_{{{camel_case}}}(h / l) = {J_hl}')
    print_abs_fact_error(J_h, fr'J_{{{camel_case}}}(h)', col2)
    print_relative_abs_error(J_h, col3)
    print_abs_fact_error(J_hl, fr'J_{{{camel_case}}}(h / l)', col2)
    print_relative_abs_error(J_hl, col3)
    J_os = print_runge(J_h, J_hl, 0, col1)
    print_abs_fact_error(J_os, fr'\overline{{J}}', col2)
    print_relative_abs_error(J_os, col3)


print_method("СКФ левых прямоугольников", "left_rect", 0)
print_method("СКФ правых прямоугольников", "right_rect", 0)
print_method("СКФ средних прямоугольников", "middle_rect", 1)
print_method("СКФ трапеций", "trapezoid", 1)
print_method("СКФ Симпсона", 'simpson', 3)