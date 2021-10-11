from typing import Callable


def detekt_root_segments(A, B, F: Callable, N, show_segments: bool = True) -> list:
    h = (B - A) / N
    position = A
    previous_calculation = F(A)
    root_segments = []
    while position < B:
        position += h
        new_calculation = F(position)
        if previous_calculation * new_calculation <= 0:
            segment = [position - h, position]
            root_segments.append(segment)
            if show_segments:
                print(f'Found segment: {segment}')
        previous_calculation = new_calculation
    return root_segments
