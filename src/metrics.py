import numpy as np
from pymoo.indicators.hv import HV

def calculate_hypervolume(front, reference_point):
    # front: lista obiektów Path z .metrics = [min1, min2, min3]
    objective_matrix = np.array([ind.metrics for ind in front])
    hv = HV(ref_point=np.array(reference_point))
    return hv(objective_matrix)
