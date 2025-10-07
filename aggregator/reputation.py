import numpy as np
def compute_reputation(scores):
    arr = np.array(scores, dtype=float)
    if arr.sum() == 0:
        return np.ones_like(arr) / len(arr)
    w = arr / arr.sum()
    return w
