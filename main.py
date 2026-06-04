"""
main.py — Entry point for the Shortest Path Snippet Judge.

Reads K C++ snippets from stdin, evaluates each one against the
mathematically correct shortest-path distance, and prints the
percentage deviation or INVALID for each snippet.

Usage:
    cat input.txt | python3 main.py
"""

import sys
from parser import extract_all_snippets, extract_time_variable, extract_final_number
from calculator import calculate_true_distance
from runner import compile_and_run


def main():
    """
    Main evaluation loop.

    For each snippet:
      A. Extract the integer value of t from source
      B. Compute the correct distance C using the ground-truth formula
      C. Compile and execute the snippet
      D. Extract the last numerical value S from the snippet's output
      E. Compute deviation = |S - C| / C * 100 and print result
    """
    raw_input = sys.stdin.read()
    snippets = extract_all_snippets(raw_input)

    for idx, snippet in enumerate(snippets, start=1):
        t_val = extract_time_variable(snippet)
        if t_val is None:
            print(f"Snippet {idx}: INVALID")
            continue

        C = calculate_true_distance(t_val)
        if C is None:
            print(f"Snippet {idx}: INVALID")
            continue

        console_log = compile_and_run(snippet, timeout_sec=10.0)
        if console_log is None:
            print(f"Snippet {idx}: INVALID")
            continue

        S = extract_final_number(console_log)
        if S is None:
            print(f"Snippet {idx}: INVALID")
            continue

        deviation = (abs(S - C) / C) * 100
        print(f"Snippet {idx}: {deviation:.2f}%")


if __name__ == "__main__":
    main()
