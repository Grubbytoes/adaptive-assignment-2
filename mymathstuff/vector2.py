import numpy as np

# This script defines function to make 2d vector logic easier
def vec2_rotated(v: np.ndarray, degrees):
    # create our rotation matrix
    theta = np.radians(degrees)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array(
        ((cos_theta, -sin_theta), (sin_theta, cos_theta))
    )
    
    # do the rotation
    return rotation_matrix.dot(v)

def vec2_magnitude(v: np.ndarray):
    raw = np.sum(np.square(v))
    return np.sqrt(raw)

def vec2_normalized(v: np.ndarray):
    return np.divide(v, vec2_magnitude(v))