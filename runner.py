import subprocess
import os
import uuid
from typing import Optional

def compile_and_run(snippet_code: str, timeout_sec: float = 2.0) -> Optional[str]:
    """
    Compiles the code snippet with C++17 and executes it securely.
    Returns console stdout/stderr on success, or None if an execution error occurs.
    """
    # Use a unique identifier to prevent execution name collisions
    unique_id = uuid.uuid4().hex
    src_file = f"temp_{unique_id}.cpp"
    bin_file = f"temp_{unique_id}.exe" if os.name == 'nt' else f"./temp_{unique_id}"
    out_bin = f"temp_{unique_id}.exe" if os.name == 'nt' else f"temp_{unique_id}"

    # Write the student's snippet code block to disk
    with open(src_file, "w", encoding="utf-8") as f:
        f.write(snippet_code)

    try:
        # 1. Compile step via C++17 standard [cite: 51]
        compile_cmd = ["g++", "-std=c++17", src_file, "-o", out_bin]
        compile_res = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5.0)
        
        if compile_res.returncode != 0:
            return None  # Compilation failed [cite: 65]

        # 2. Execution step with built-in time-limit guardrails [cite: 67]
        exec_res = subprocess.run([bin_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_sec)
        
        if exec_res.returncode != 0:
            return None  # Program crashed at runtime [cite: 66]

        # Combine standard streams to catch all output statements [cite: 46, 48]
        return exec_res.stdout.decode('utf-8', errors='ignore') + "\n" + exec_res.stderr.decode('utf-8', errors='ignore')

    except subprocess.TimeoutExpired:
        return None  # Caught an infinite loop, safely terminated [cite: 61]
    finally:
        # File management: clean up all temporary storage footprint files from the disk
        if os.path.exists(src_file):
            os.remove(src_file)
        if os.path.exists(out_bin):
            os.remove(out_bin)
