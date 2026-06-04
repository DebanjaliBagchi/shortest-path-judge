"""
parser.py — Input parsing and output extraction utilities.

Handles three jobs:
1. Splitting the input file into individual C++ snippets
2. Extracting the integer value of t from snippet source code
3. Extracting the last valid numerical value from program output
"""

import re
from typing import List, Optional


def extract_all_snippets(input_text: str) -> List[str]:
    """
    Split the input into individual C++ code blocks.

    Looks for code enclosed between BEGIN_SNIPPET and END_SNIPPET markers.

    Args:
        input_text: The full input string (first line is K, then snippets).

    Returns:
        List of source code strings, one per snippet.
    """
    return re.findall(r'BEGIN_SNIPPET\n(.*?)\nEND_SNIPPET', input_text, re.DOTALL)


def extract_time_variable(snippet_code: str) -> Optional[int]:
    """
    Parse the C++ source to find the integer value assigned to variable t.

    Supports these declaration forms:
        auto t = X;
        int t = X;
        long long t = X;
        const int t = X;
        constexpr int t = X;
        constexpr auto t = X;
        int t{X};          (brace initialization)
        #define t X

    Falls back to matching bare assignment: t = X;

    Args:
        snippet_code: The raw C++ source code of one snippet.

    Returns:
        The integer value of t, or None if it cannot be determined.
        Returns None for indirect assignments like `int t = val;` where
        val is not an integer literal — this is a known limitation matching
        the problem spec's stated forms.
    """
    patterns = [
        r'\b(?:constexpr\s+)?(?:auto|int|long\s+long|long)\s+t\s*=\s*(-?\s*\d+)',
        r'\b(?:const\s+)?(?:auto|int|long\s+long|long)\s+t\s*=\s*(-?\s*\d+)',
        r'\b(?:constexpr\s+)?(?:auto|int|long\s+long|long)\s+t\s*\{\s*(-?\s*\d+)\s*\}',
        r'\b(?:const\s+)?(?:auto|int|long\s+long|long)\s+t\s*\{\s*(-?\s*\d+)\s*\}',
        r'#define\s+t\s+(-?\s*\d+)',
        r'\bt\s*=\s*(-?\s*\d+)\s*;',
    ]

    for pattern in patterns:
        match = re.search(pattern, snippet_code)
        if match:
            val_str = match.group(1).replace(" ", "")
            try:
                return int(val_str)
            except ValueError:
                continue

    return None


def extract_final_number(console_output: str) -> Optional[float]:
    """
    Extract the last valid numerical value from program output.

    The problem states: "The final numerical value printed during program
    execution must be treated as the snippet-generated shortest-path value."

    Matches integers, floats, and scientific notation (e.g. 3.14, -7, 1.5e-3).
    Filters out nan and inf which indicate broken computation.

    Args:
        console_output: Combined stdout+stderr text from the executed snippet.

    Returns:
        The last parseable number as a float, or None if no valid number found.
    """
    if not console_output or not console_output.strip():
        return None

    numbers = re.findall(r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', console_output)

    if not numbers:
        return None

    try:
        val = float(numbers[-1])
        if val != val:
            return None
        if abs(val) == float('inf'):
            return None
        return val
    except (ValueError, OverflowError):
        return None
