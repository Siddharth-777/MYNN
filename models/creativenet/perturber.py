# perturber.py
import numpy as np

def perturb_vector(vec, noise_level=0.1):
    noise = np.random.normal(0, noise_level, size=vec.shape)
    return vec + noise
