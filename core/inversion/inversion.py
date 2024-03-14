# Rdz 1, 3
import numpy as np


def inversion(chromosome : str) -> str:
    inversion_points = sorted(np.random.randint(low=0, high=len(chromosome), size=2))
    anaphase = [*chromosome]
    while inversion_points[1] > inversion_points[0]:
        anaphase[inversion_points[0]], anaphase[inversion_points[1]] = anaphase[inversion_points[1]], anaphase[inversion_points[0]]
        inversion_points[0] += 1
        inversion_points[1] -= 1

    return ''.join(anaphase)