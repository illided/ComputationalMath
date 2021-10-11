from task1 import SimpleReverseInterpolation, RootSearchReverseInterpolation
from vichi_2.launcher import create_table
import numpy as np
import matplotlib.pyplot as plt


function = 'exp(x) + sin(x)'

X_t, Y_t = create_table(10, (0, 10), function)

ri = RootSearchReverseInterpolation(X_t, Y_t)
print(ri.interpolate(3.21))
