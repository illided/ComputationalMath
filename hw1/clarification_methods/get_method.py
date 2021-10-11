from clarification_methods.newton_method import NewtonMethod
from clarification_methods.modified_newton_method import ModifiedNewtonMethod
from clarification_methods.bisection_method import BisectionMethod
from clarification_methods.secant_method import SecantMethod

method_map = {
    'newton': NewtonMethod,
    'bisection': BisectionMethod,
    'modified_newton': ModifiedNewtonMethod,
    'secant': SecantMethod
}


def get_clarification_method(sym_expr, kind: str = 'newton', **kwargs):
    return method_map[kind](sym_expr, **kwargs)
