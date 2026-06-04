"""
runner.py — Safe C++ compilation and execution with timeout protection.

Compiles a C++ snippet using g++ (C++17), executes the resulting binary,
captures combined stdout/stderr output, and cleans up temporary files.
Handles infinite loops via timeout, and crashes via exit code checks.
"""

import subprocess
import os
import uuid
from typing import Optional


def compile_and_run(snippet_code: str, timeout_sec: float = 10.0) -> Optional[str]:
    """
    Compile and execute a C++ snippet in a sandboxed temporary environment.

    The snippet is written to a temp file, compiled with g++ -std=c++17,
    executed with a time limit, and the temp files are cleaned up regardless
    of outcome.

    Args:
        snippet_code: Complete C++ source code to compile and run.
        timeout_sec:  Maximum execution time in seconds. Snippets exceeding
                      this are killed and treated as INVALID. Default: 10s.

    Returns:
        Combined stdout + stderr as a string on success.
        None if compilation fails, execution crashes, or timeout is exceeded.
    """
    unique_id = uuid.uuid4().hex
    src_file = f"temp_{unique_id}.cpp"
    bin_file = f"temp_{unique_id}.exe" if os.name == 'nt' else f"./temp_{unique_id}"
    out_bin = f"temp_{unique_id}.exe" if os.name == 'nt' else f"temp_{unique_id}"

    with open(src_file, "w", encoding="utf-8") as f:
        f.write(snippet_code)

    try:
        include_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "include"
        )
        if not os.path.isdir(include_dir):
            include_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "solution", "include"
            )
        compile_cmd = ["g++", "-std=c++17", f"-I{include_dir}", src_file, "-o", out_bin]
        compile_res = subprocess.run(
            compile_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30.0
        )

        if compile_res.returncode != 0:
            return None

        exec_res = subprocess.run(
            [bin_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_sec
        )

        if exec_res.returncode != 0:
            return None

        stdout_text = exec_res.stdout.decode('utf-8', errors='ignore')
        stderr_text = exec_res.stderr.decode('utf-8', errors='ignore')
        return stdout_text + "\n" + stderr_text

    except subprocess.TimeoutExpired:
        return None

    finally:
        if os.path.exists(src_file):
            os.remove(src_file)
        if os.path.exists(out_bin):
            os.remove(out_bin)
