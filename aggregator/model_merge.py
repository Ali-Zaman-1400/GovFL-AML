import numpy as np, torch
def average_weights(local_models, weights):
    keys = list(local_models[0].keys())
    avg = {}
    for k in keys:
        params = [local[k].float() for local in local_models]
        stacked = torch.stack(params, dim=0)
        w = torch.tensor(weights, dtype=stacked.dtype).view(-1, *([1]*(stacked.dim()-1)))
        avg[k] = (stacked * w).sum(dim=0)
    return avg
