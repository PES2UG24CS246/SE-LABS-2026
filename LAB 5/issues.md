# Lab 5: Static Code Analysis — Issues and Fixes

## Initial Analysis Results

- Pylint score before fixes: 4.48/10
- Bandit findings before fixes: 5 potential security issues
- Flake8: Multiple style and code-quality violations

## Issues Identified and Fixed

| No. | Issue | Problem | Fix Applied |
|---|---|---|---|
| 1 | Unsafe eval() usage | Could execute arbitrary Python expressions. | Replaced with a restricted AST-based arithmetic evaluator. |
| 2 | Weak MD5 hashing | MD5 is unsuitable for security-sensitive hashing. | Replaced MD5 with SHA-256. |
| 3 | Hardcoded supervisor password | Credentials were stored directly in source code. | Read the password from an environment variable. |
| 4 | Mutable default argument | A default list could be shared across function calls. | Changed the default value to None. |
| 5 | Bare except block | Errors could be silently ignored. | Added explicit validation and removed silent exception handling. |
| 6 | Unsafe file handling | Files were not consistently managed with context managers. | Used with statements and UTF-8 encoding. |
| 7 | Unused imports and variables | Unnecessary names reduced code clarity. | Removed unused imports and variables. |
| 8 | Inconsistent naming and formatting | Code style was inconsistent. | Used snake_case naming and improved formatting. |
| 9 | Unnecessary global statement | Rebinding the stock dictionary was unnecessary. | Updated the existing dictionary using clear() and update(). |

## Final Verification

- Pylint: 10.00/10
- Bandit: No issues identified
- Flake8: No violations printed
- Program execution: Completed successfully

The final version improved code readability, maintainability, input validation, file handling, and security.
