import sys
from parser import extract_all_snippets, extract_time_variable, extract_final_number
from calculator import calculate_true_distance
from runner import compile_and_run

def main():
    # Read all payload data passing through standard input streams [cite: 98]
    raw_input = sys.stdin.read()
    
    # Isolate all standard C++ code snippets present [cite: 26]
    snippets = extract_all_snippets(raw_input)
    
    for idx, snippet in enumerate(snippets, start=1):  # 1-indexed tracking [cite: 89]
        # Step A: Parse out target time variable value 't'
        t_val = extract_time_variable(snippet)
        if t_val is None:
            print(f"Snippet {idx}: INVALID")  # [cite: 96]
            continue
            
        # Step B: Calculate true mathematical shortest path reference distance 'C'
        C = calculate_true_distance(t_val)
        if C is None:
            print(f"Snippet {idx}: INVALID")
            continue

        # Step C: Send the isolated code to compile and run safely inside the sandbox
        console_log = compile_and_run(snippet, timeout_sec=2.0)
        if console_log is None:
            print(f"Snippet {idx}: INVALID")  # [cite: 96]
            continue

        # Step D: Process printed output to extract the computed distance 'S'
        S = extract_final_number(console_log)
        if S is None:
            print(f"Snippet {idx}: INVALID")  # [cite: 94, 96]
            continue

        # Step E: Apply the mandatory Deviation Formula [cite: 81, 82, 83, 84]
        deviation = (abs(S - C) / C) * 100
        
        # Output exactly matches required specifications: rounded to 2 decimal places [cite: 87, 90]
        print(f"Snippet {idx}: {deviation:.2f}%")

if __name__ == "__main__":
    main()
