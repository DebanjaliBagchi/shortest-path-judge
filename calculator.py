"""
calculator.py — Ground-truth shortest-path distance computation.

Computes the correct distance from V1 to V10 for a given integer t.
Since the graph is fully connected with Euclidean edge weights, the
shortest path is always the direct edge (triangle inequality guarantee).
This lets us compute the answer in O(1) without running Dijkstra.
"""

import math


def calculate_true_distance(t: int) -> float:
    """
    Compute the correct shortest-path distance from V1 to V10.

    Uses the direct Euclidean distance formula, which is equivalent to
    running Dijkstra on the complete graph (triangle inequality ensures
    no multi-hop path is shorter than the direct edge).

    Args:
        t: Integer time parameter that defines vertex coordinates.
           Must satisfy t > -2 for all log arguments to be positive.

    Returns:
        The Euclidean distance between V1 and V10 as a float.
        Returns None if t causes a math domain error (log of non-positive).
    """
    for i in range(1, 11):
        if i + t + 1 <= 0:
            return None

    try:
        x1 = math.sin(1 * t) + 1
        y1 = math.cos(1 * t) + 1**2
        z1 = math.log(1 + t + 1)

        x10 = math.sin(10 * t) + 10
        y10 = math.cos(10 * t) + 10**2
        z10 = math.log(10 + t + 1)

        distance = math.sqrt(
            (x1 - x10)**2 + (y1 - y10)**2 + (z1 - z10)**2
        )
        return distance

    except (ValueError, OverflowError):
        return None
