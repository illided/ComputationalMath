from sympy import parse_expr, lambdify, diff
from clarification_methods.get_method import get_clarification_method
from segmentation import detekt_root_segments

A = -15
B = -10
e = 10 ** (-11)
N = 100
F_string = '5 * sin(2 * x) - sqrt(1 - x)'
max_num_of_iterations = 20000000000000000
kinds = ['newton', 'modified_newton', 'secant', 'bisection']

sym_F = parse_expr(F_string)
sym_dF = diff(sym_F)

F = lambdify('x', sym_F)
dF = lambdify('x', sym_dF)


def greeting():
    print(f"Решение нелинейного уравнения с помощью отделения корней и уточнения.\n"
          f"Параметры: A = {A}, B = {B}, N = {N}, эпсилон = {e}\n"
          f"Функция: {F_string}\n")


def main():
    greeting()
    print("\nStarting root segmentation")
    segments = detekt_root_segments(A, B, F, N)
    print()
    for segment in segments:
        print(f"-------- Clarifying segment {segment} ---------")
        for kind in kinds:
            print(f'Clarifying segment with {kind} method')
            clarification_method = get_clarification_method(sym_F,
                                                            kind=kind,
                                                            max_iteration=max_num_of_iterations,
                                                            e=e,
                                                            print_iterations=False)
            root = clarification_method.compute(segment)
            if clarification_method.finished:
                print('\033[1m' + f"Root found: {root}" + '\033[0m')
            else:
                print(f'Failed to find root. Last approximation: {root}')
            print(f'Num of iterations: {clarification_method.iterations_passed}\n'
                  f'Error: {clarification_method.get_error()}\n'
                  f'Last clarification: {clarification_method.get_clarification()}\n')


if __name__ == "__main__":
    main()
