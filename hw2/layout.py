import streamlit as st


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represents_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_region():
    col1, col2 = st.columns(2)
    a = col1.text_input(label="Введите a - левую границу")
    b = col2.text_input(label="Введите b - правую границу")
    need_stop = False
    if not a:
        need_stop = True
    elif not represents_float(a):
        col2.warning("Неправильный формат числа с плавающей запятой")
        need_stop = True
    if not b:
        need_stop = True
    elif not represents_float(b):
        col1.warning("Неправильный формат числа с плавающей запятой")
        need_stop = True
    if not need_stop and a > b:
        st.warning("Левая граница должна быть меньше правой")
        need_stop = True
    if need_stop:
        st.stop()
    return float(a), float(b)


def get_interpolation_parameters(table_size: int, variable: str = 'x'):
    col1, col2 = st.columns(2)
    v = col1.text_input(label=f"Введите {variable} - параметр задачи")
    n = col2.text_input(label="Введите n - степень многочлена")
    need_stop = False
    if not n:
        need_stop = True
    elif not represents_int(n):
        col2.warning("Неправильный формат натурального числа")
        need_stop = True
    if not v:
        need_stop = True
    elif not represents_float(v):
        col1.warning("Неправильный формат числа с плавающей запятой")
        need_stop = True
    if not need_stop and int(n) > int(table_size) - 1:
        st.warning(f"Степень многочлена должна быть меньше {int(table_size)}")
        need_stop = True
    if need_stop:
        st.stop()

    v = float(v)
    n = int(n)

    return v, n


def get_table_size():
    t_s = st.text_input(label="Введите число значений в таблице")
    if not t_s:
        st.stop()
    if not represents_int(t_s):
        st.warning("Неправильный формат числа")
        st.stop()
    return int(t_s)
