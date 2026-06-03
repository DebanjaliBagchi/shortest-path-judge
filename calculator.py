import math

def calculate_true_distance(t: int) -> float:
    """
    Computes the mathematically correct direct Euclidean distance
    between vertex V1 and vertex V10 in O(1) time.
    """
    try:
        # Vertex 1 Coordinates (i = 1)
        x1 = math.sin(1 * t) + 1             # [cite: 11]
        y1 = math.cos(1 * t) + 1**2          # [cite: 12]
        z1 = math.log(1 + t + 1)             # [cite: 13]
        
        # Vertex 10 Coordinates (i = 10)
        x10 = math.sin(10 * t) + 10          # [cite: 11]
        y10 = math.cos(10 * t) + 10**2       # [cite: 12]
        z10 = math.log(10 + t + 1)           # [cite: 13]
        
        # Euclidean Distance: sqrt((x1-x10)^2 + (y1-y10)^2 + (z1-z10)^2)
        distance = math.sqrt((x1 - x10)**2 + (y1 - y10)**2 + (z1 - z10)**2)  # [cite: 20]
        return distance
    except (ValueError, OverflowError):
        # Triggers if log() encounters a value <= 0 due to negative values of t
        return None
