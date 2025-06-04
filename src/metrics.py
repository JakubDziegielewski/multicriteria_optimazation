import numpy as np
from pymoo.indicators.hv import HV

def calculate_hypervolume(front, reference_point: list[float]) -> float:
    """
    Oblicz hypervolume dla danego frontu.
    Wszystkie cele powinny być minimalizowane!
    """
    objective_matrix = np.array([ind.metrics for ind in front])
    hv = HV(ref_point=np.array(reference_point))
    return hv(objective_matrix)
