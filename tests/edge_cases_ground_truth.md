# Edge Cases Ground Truth

## Correct Distance Values

| t | C (Correct Distance) |
|---|---|
| 5 | 100.1552235482 |
| 0 | 99.4228654086 |
| -1 | 98.1985081202 |
| -2 | UNDEFINED (log domain error) |
| 999999 | 99.7396926998 |
| 1000000 | 97.6460313506 |
| -1000000 | UNDEFINED (log domain error) |

---

## Expected Output

```
Snippet 1: 0.00%
Snippet 2: 0.00%
Snippet 3: 0.00%
Snippet 4: INVALID
Snippet 5: 0.00%
Snippet 6: INVALID
Snippet 7: INVALID
Snippet 8: INVALID
Snippet 9: INVALID
Snippet 10: INVALID
Snippet 11: 898.18%
Snippet 12: 0.00%
Snippet 13: 0.00%
Snippet 14: 0.00%
Snippet 15: 5.00%
Snippet 16: 100.00%
Snippet 17: 9915.52%
Snippet 18: 200.00%
Snippet 19: 100.00%
Snippet 20: 998448157498498.69%
Snippet 21: 0.00%
Snippet 22: 0.00%
Snippet 23: 0.00%
Snippet 24: 10.03%
Snippet 25: 0.00%
Snippet 26: INVALID
Snippet 27: INVALID
Snippet 28: INVALID
Snippet 29: INVALID
Snippet 30: 0.00%
```

---

## Case-by-Case Description

| # | t | Category | Description | Expected |
|---|---|---|---|---|
| 1 | 5 | Correct | Perfect Dijkstra implementation | 0.00% |
| 2 | 0 | Correct | Perfect Dijkstra, t=0 (sin/cos all 0/1) | 0.00% |
| 3 | -1 | Correct | Perfect Dijkstra, t=-1 (boundary: log(1)=0) | 0.00% |
| 4 | -2 | Invalid t | log(0) undefined → produces nan/inf → INVALID | INVALID |
| 5 | 999999 | Correct | Perfect Dijkstra, large t | 0.00% |
| 6 | 5 | Timeout | `while(true)` infinite loop | INVALID |
| 7 | 5 | Runtime crash | nullptr dereference → segfault | INVALID |
| 8 | 5 | Compile error | Missing semicolons in source | INVALID |
| 9 | 5 | No output | Prints "Done processing" (no number) | INVALID |
| 10 | 5 | No output | Prints empty string | INVALID |
| 11 | 5 | Wrong formula | Y = cos(i*t) + i³ instead of i² | 898.18% |
| 12 | 5 | Bug (benign) | Floyd-Warshall wrong loop order (i,j,k vs k,i,j) — but Euclidean complete graph means direct edge is always shortest, so result is still correct | 0.00% |
| 13 | 5 | Tricky t | `int val = 5; int t = val;` — indirect assignment | 0.00% |
| 14 | 5 | Correct | Bellman-Ford with `constexpr int t = 5` | 0.00% |
| 15 | 5 | Scaled wrong | Correct answer × 1.05 | 5.00% |
| 16 | 5 | Scaled wrong | Correct answer × 2.0 | 100.00% |
| 17 | 5 | Forgot sqrt | Outputs distance² instead of distance | 9915.52% |
| 18 | 5 | Negative | Outputs −C (negated correct answer) | 200.00% |
| 19 | 5 | Zero output | Hardcodes output as 0.0 | 100.00% |
| 20 | 5 | Sentinel | Outputs 1e18 (unreachable sentinel) | ~10^15 % |
| 21 | 5 | stderr only | Prints correct answer to cerr, nothing to cout | 0.00% |
| 22 | 5 | Multi-number | Prints "Step1=3.14 Step2=2.71 Final=C" — last number is correct | 0.00% |
| 23 | 5 | Correct | Floyd-Warshall with CORRECT loop order (k,i,j) | 0.00% |
| 24 | 5 | Wrong metric | Manhattan distance instead of Euclidean | 10.03% |
| 25 | 10⁶ | Boundary | Maximum allowed positive t | 0.00% |
| 26 | -10⁶ | Invalid t | log argument negative → INVALID | INVALID |
| 27 | 5 | Runtime crash | `throw runtime_error` → non-zero exit | INVALID |
| 28 | 5 | Runtime crash | `exit(1)` → non-zero exit code | INVALID |
| 29 | 5 | OOM attempt | Allocates 1 billion ints → may crash OR succeed (OS dependent). On macOS with overcommit, vector is zeroed and outputs 0 → 100.00%. On systems that reject alloc → INVALID | 100.00% or INVALID |
| 30 | 5 | Correct | Direct Euclidean (valid shortcut) | 0.00% |

---

## Edge Cases That Test Parser Robustness

| Test | What it checks |
|---|---|
| Snippet 3 | `long long t = -1` — type variant |
| Snippet 13 | `int val = 5; int t = val;` — parser must find `t = val` then `val = 5`, OR directly match `int t = val` where val isn't a literal. This should work if parser follows the `\bt\s*=\s*(-?\d+)` fallback |
| Snippet 14 | `constexpr int t = 5` — constexpr qualifier |
| Snippet 21 | Output on stderr only — judge must check both streams |
| Snippet 22 | Multiple numbers in output — must take the LAST one |
| Snippet 4, 26 | Negative t causing math domain errors |

---

## Notes

- Snippet 4 (t=-2): The snippet will likely produce `nan` or `-inf` from `log(0)`. 
  Depending on implementation, the program may run but output `nan` which is not a valid number → INVALID.
  Alternatively, your judge computes C and finds log domain error → INVALID regardless.
  
- Snippet 12: Floyd-Warshall with wrong loop order (i,j,k instead of k,i,j) is a classic bug. 
  However, in a complete Euclidean graph, direct edges satisfy the triangle inequality, 
  so the shortest path is always the direct edge. Even the broken FW will report dist[1][10] 
  correctly because the initial direct edge weight is already optimal.

- Snippet 13: Tests if parser can handle `int t = val` where val is previously defined. 
  Simple regex parsers will FAIL this. The fallback pattern `\bt\s*=\s*(-?\d+)` won't match 
  since `val` is not a digit. Your parser should either:
  - Handle this gracefully as INVALID (can't determine t), OR
  - Be smart enough to trace the assignment chain.
  
  **For the simple judge**: reporting INVALID is acceptable here since the problem says 
  t appears in forms like `auto t = X` where X is an integer.
