import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (a, b, c).
    b is the vertex (the joint).
    """
    a = np.array(a) # Proximal point (e.g., Wrist)
    b = np.array(b) # Joint of interest (e.g., MCP)
    c = np.array(c) # Distal point (e.g., PIP)
    
    # Create vectors
    ba = a - b
    bc = c - b
    
    # Calculate cosine angle using dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    
    # Convert to degrees
    degree = np.degrees(angle)
    
    # Clinical adjustment: 
    # In math, straight line is 180. In medicine, straight finger is 0 flexion.
    # So we return 180 - degree.
    return 180 - degree