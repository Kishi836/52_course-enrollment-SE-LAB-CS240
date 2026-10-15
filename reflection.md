# Reflection: Static Code Analysis

Static analysis took this file from 4.00/10 to a clean 10.00/10, with zero Bandit and Flake8 findings. But all three tools missed the bug that actually printed wrong output: dropping a student from CS202 reopened a full course that nobody was enrolled in, so the program reported 3 open courses instead of 2. That gap shapes every answer below.

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the ones where the tool's message was also the fix. Unused imports and variables, `== None`, missing docstrings, camelCase names and long lines were mechanical, and each was a single local edit.

The hardest were the issues where the fix changed the program's interface rather than one line. `eval(discount_expr)` cannot be patched in place. The function accepted arbitrary code, so I had to decide what it should accept instead: a discount percentage, validated to be between 0 and 100. Its caller had to change too. Hardest of all was the drop bug, which no tool reported. Fixing it meant giving each course a list of enrolled students. Only then could `drop_course` check that the student was actually enrolled, and total tuition be derived from enrollments so that a drop refunds it.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Mostly no. Every Bandit finding was a real risk in this file. The token was not just hardcoded but printed to stdout, and the OTP really did need a secure random source. The closest thing to a false positive was Pylint's C0103 on `total_tuition`. Pylint treats any module-level variable as a constant and wants UPPER_CASE, but this was mutable running state, so renaming it would have been wrong. The real fix was removing the global altogether. B324 (MD5) is also context-dependent: if the hash were only a non-security identifier, `usedforsecurity=False` would be acceptable.

The tools also disagree with each other. Pylint allows 100-character lines and Flake8 allows 79, so code that is clean in Pylint still fails Flake8. That is why the Flake8 fixes ended up in a separate commit.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally, before commit:** a pre-commit hook running Flake8 and Bandit, which are fast enough to run on every commit.
- **In CI:** a GitHub Actions job on every push and pull request running `pylint --fail-under=9.5`, `bandit -r . -ll` (fail on medium severity and above) and `flake8`, so that a regression blocks the merge.
- **Shared configuration:** one `setup.cfg`/`pyproject.toml` that sets the same line length for both linters and records every deliberately ignored rule, so that suppressions are reviewed rather than silent.

None of this replaces tests. The drop bug would only be caught by a test that asserts the open-course count after an invalid drop.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** both code-execution paths (`os.system` on a filename and `eval` on caller input) are gone, the secret moved out of source into an environment variable, and the hash and OTP now use SHA-256 and `secrets`.
- **Robustness:** the shared `audit_trail=[]` default no longer leaks entries between calls, errors are no longer swallowed by `except: pass`, and the roster file is closed even if writing fails.
- **Correctness:** an invalid drop no longer frees a seat, duplicate enrollment is rejected, tuition is refunded on a drop, and the exported roster now lists the enrolled students.
- **Readability:** snake_case names, docstrings, and a one-line `check_course_status` in place of a nested if/else. Running `main()` only under `__main__` makes the module importable, which is what let me check the fixes with assertions.
