import torch
def add_noise(model, epsilon=3.0):
    # Laplace-like noise scaled by epsilon (simple simulation)
    for p in model.parameters():
        noise = torch.randn_like(p) * (1.0 / max(epsilon, 1e-6))
        p.data += noise
