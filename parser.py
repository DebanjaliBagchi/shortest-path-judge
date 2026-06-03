import re
from typing import List, Optional

def extract_all_snippets(input_text: str) -> List[str]:
    """Isolates all code blocks enclosed within BEGIN_SNIPPET and END_SNIPPET."""
    # [cite: 100, 101]
    return re.findall(r'BEGIN_SNIPPET\n(.*?)\nEND_SNIPPET', input_text, re.DOTALL)

def extract_time_variable(snippet_code: str) -> Optional[int]:
    """ Parses the C++ initialization line to extract the value of variable t. """
    # Supports variations like: auto t=X, int t=X;, long long t=X with arbitrary spaces [cite: 33, 34, 35]
    pattern = r'\b(?:auto|int|long\s+long)\s+t\s*=\s*(-?\s*\d+)'
    match = re.search(pattern, snippet_code)
    if match:
        # Clean potential whitespaces inside negative numbers (e.g., "- 5" -> "-5")
        return int(match.group(1).replace(" ", ""))
    return None

def extract_final_number(console_output: str) -> Optional[float]:
    """ Extracts the absolute final numerical value printed during execution. """
    # Recognizes standard integers, floating-points, and scientific notation (e.g. 1e18) [cite: 45, 136]
    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', console_output)
    if numbers:
        return float(numbers[-1])  # Returns the last number tracked [cite: 76]
    return None
