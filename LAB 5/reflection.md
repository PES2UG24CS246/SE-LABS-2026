# Lab 5: Static Code Analysis — Reflection

## 1. What did you learn about static code analysis?

I learned that static analysis tools can identify code-quality, security, and style problems without requiring the program to be executed. Pylint checks code quality, Bandit identifies potentially insecure coding patterns, and Flake8 checks style and common coding mistakes.

## 2. What were the important issues identified?

The main issues included unsafe eval() usage, a hardcoded supervisor password, weak MD5 hashing, a mutable default argument, and a bare except block. These findings showed that code can run successfully while still having security and reliability problems.

## 3. How did you fix and verify the issues?

I replaced eval() with a restricted arithmetic evaluator, moved the supervisor password to an environment variable, replaced MD5 with SHA-256, corrected the mutable default argument, and improved validation and file handling. I reran Pylint, Bandit, and Flake8 to verify the changes.

## 4. How will static analysis help in future projects?

I will use static analysis tools during development and before submitting code. These tools can help me identify problems early, improve readability, reduce security risks, and make software easier to maintain.
