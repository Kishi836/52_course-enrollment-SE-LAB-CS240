# Issues Found: `course_enrollment_system.py`

Line numbers refer to the original file (commit `c54f47d`). Baseline: Pylint 4.00/10, Bandit 6 issues (2 High, 1 Medium, 3 Low), Flake8 12 issues. Final: Pylint 10.00/10, Bandit 0, Flake8 0.

## High and medium severity

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 63 | `os.system("echo ... " + filename)` builds a shell command from a parameter; a filename like `x.txt & del /q *` runs arbitrary commands | Replaced with `print()`; no shell is needed to show a message |
| Weak hash (Bandit B324, High) | Security | 52 | Student hash uses MD5, which is broken for security use | Switched to `hashlib.sha256` |
| Use of `eval` (Bandit B307 Medium, Pylint W0123) | Security | 47 | `calculateScholarshipTuition` evaluates a caller-supplied string as Python, so any expression (e.g. `__import__('os').system(...)`) runs | Takes a numeric `discount_percent`, validates 0–100, computes `fee * (1 - pct/100)` |
| Mutable default argument (Pylint W0102) | Bug | 15 | `audit_trail=[]` is created once and shared across every call, so audit entries leak between enrollments | Default to `None` and create a new list inside the function |
| Drop reopens courses with no enrollment (not flagged by any tool) | Bug | 27–32, 83 | `dropCourse("CS202")` added a seat and reopened a full course nobody had enrolled in, so output said **Open courses: 3** instead of 2; drops never refunded tuition | Courses track enrolled `students`; drop requires an enrolled student; duplicate enrollment rejected; total tuition derived from enrollments |
| Hardcoded secret (Bandit B105) | Security | 75, 84 | Registrar token is in source code and printed to stdout | Read from `REGISTRAR_AUTH_TOKEN` env var; only print whether it is set |
| Insecure OTP randomness (Bandit B311) | Security | 56 | `random.randint` is predictable, unfit for OTPs | `1000 + secrets.randbelow(9000)` |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Bug | 31–32 | Swallows every error silently, including typos and `KeyboardInterrupt` | Explicit `if course_id not in courses: return False` |
| Global state (Pylint W0603) | Design | 12, 16 | `global total_tuition` mutated in place and never read | Removed; `calculate_total_tuition()` computes it from enrollments |
| File opened without `with`/encoding (Pylint R1732, W1514) | Bug | 60–62 | File leaks if `write` raises; encoding is platform-dependent | `with open(filename, "w", encoding="utf-8")` |

## Low severity / style

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Unused import / variables (Pylint W0611, W0612; Flake8 F401, F841) | Style | 4, 36, 46, 68 | `math`, `lab_fee`, `base_fee` (eval-only), `cid` unused | Removed |
| Shadowed global (Pylint W0621) | Style | 66 | Parameter `courses` hides the module-level dict | Renamed to `catalog` |
| `== None` and redundant if/else (Pylint C0121, R1703, R1705; Flake8 E711) | Style | 37–42 | Comparison to `None` with `==`; if/else returning booleans | `return course is not None and not course["is_closed"]` |
| camelCase names (Pylint C0103) | Style | 15–66 | Function names not snake_case | Renamed, e.g. `enrollStudent` → `enroll_student` |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, all functions | No module or function docstrings | Added |
| `%` formatting (Pylint C0209) | Style | 23 | Old-style string formatting | f-string |
| Line too long (Pylint C0301, Flake8 E501) | Style | 7–9, 15, 23, 79 | Lines over 79 chars (Flake8) / 100 chars (Pylint) | Wrapped |
| Missing final newline, unguarded `main()` (Pylint C0304, Flake8 W292) | Style | 87 | No trailing newline; `main()` runs on import | Added newline; `if __name__ == "__main__":` guard |
