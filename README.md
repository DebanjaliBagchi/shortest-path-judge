# Shortest Path Judge

A Python-based judge that evaluates C++ code snippets attempting to solve a shortest-path problem on a parameterized 10-vertex 3D graph.

## Problem

Given K independent C++ snippets, each computing the shortest-path distance from vertex V1 to V10 on a fully-connected directed graph with Euclidean edge weights in 3D space, this judge:

1. Extracts the integer parameter `t` from each snippet's source code
2. Computes the mathematically correct shortest-path distance
3. Compiles and executes the snippet safely (with timeout protection)
4. Extracts the snippet's numerical output
5. Reports the percentage deviation from the correct answer

## Graph Specification

For a given integer `t`, vertex `Vi` has coordinates:
- `Xi = sin(i * t) + i`
- `Yi = cos(i * t) + i²`
- `Zi = log(i + t + 1)`

Edge weight between any two vertices is the 3D Euclidean distance. The graph contains exactly 90 directed edges (complete graph, 10 vertices).

## Usage

### Basic (reads from stdin)

```bash
cat input.txt | python3 main.py
```

### Running on test files

```bash
# Run the sample input (1 snippet)
cat tests/sample_input.txt | python3 main.py

# Run the full test suite (10 snippets)
cat tests/full_test.txt | python3 main.py

# Run the edge-case suite (30 snippets, comprehensive)
cat tests/edge_cases.txt | python3 main.py

# Validate against expected output
cat tests/edge_cases.txt | python3 main.py 2>/dev/null | diff - tests/edge_cases_expected.txt
```

### Using the solution judge (faster, supports arguments)

The `solution/` directory contains a full-featured judge with CLI flags:

```bash
cd ../solution

# Basic
python3 main.py tests/edge_cases.txt

# Fast (recommended)
python3 main.py tests/edge_cases.txt --timeout 3 --parallel --workers 8

# Verbose debugging
python3 main.py tests/edge_cases.txt --timeout 3 --verbose

# Validate against expected output
python3 main.py tests/edge_cases.txt --timeout 3 2>/dev/null | diff - tests/edge_cases_expected.txt
```

#### Solution judge arguments

```
python3 main.py [INPUT_FILE] [OPTIONS]

Positional:
  INPUT_FILE              Path to input file. Reads from stdin if omitted.

Options:
  --parallel              Run snippet compilation/execution in parallel threads.
  --workers N             Number of parallel workers (default: 4).
  --timeout N             Per-snippet execution timeout in seconds (default: 10).
  --compiler PATH         C++ compiler executable (default: g++).
  --verbose               Print detailed per-snippet breakdown to stderr.
```

### Performance

| Mode | Time (30 snippets) | Notes |
|------|---------------------|-------|
| This judge (sequential, 10s timeout) | ~46s | Infinite-loop snippet waits full 10s |
| Solution judge (sequential, 3s timeout) | ~12s | Lower timeout = less waiting |
| Solution judge (parallel, 8 workers, 3s) | ~13s | Best throughput |

**Recommendation**: For fast evaluation, use the solution judge with `--parallel --workers 8 --timeout 3`.

## Input Format

```
K
BEGIN_SNIPPET
<C++ code>
END_SNIPPET
BEGIN_SNIPPET
<C++ code>
END_SNIPPET
...
```

## Output Format

```
Snippet 1: 0.00%
Snippet 2: INVALID
Snippet 3: 14.73%
```

Each line is either:
- `Snippet i: XX.XX%` — deviation rounded to 2 decimal places
- `Snippet i: INVALID` — if compilation/execution/extraction failed

## Architecture

| File | Purpose |
|------|---------|
| `main.py` | Entry point — reads stdin, orchestrates the pipeline |
| `parser.py` | Extracts snippets from input, parses `t` value, extracts numerical output |
| `calculator.py` | Computes the ground-truth shortest-path distance for a given `t` |
| `runner.py` | Compiles and executes C++ snippets with timeout and crash protection |

## Requirements

- Python 3.8+
- `g++` with C++17 support
- The `include/bits/stdc++.h` header is bundled in this repo (for macOS/clang compatibility)

## Credits

The core logic of this judge was written by a human. Claude (Anthropic) was used to:
- Refactor function signatures and docstrings for clarity
- Expand the `t`-extraction parser to handle `constexpr`, `const`, brace-initialization, and `#define` variants
- Add nan/inf filtering to output extraction
- Conduct thorough edge-case analysis (30 cases covering compile errors, timeouts, crashes, math domain errors, wrong algorithms, output format variations, and boundary conditions)
- Format documentation and ground-truth files

All algorithmic decisions (using direct Euclidean distance as the ground truth, the "last number" extraction rule, the deviation formula) were made by the human author based on the problem specification.
