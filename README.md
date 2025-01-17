# django-migration-checker

A Python script to check for duplicate migration numbers across all Django apps in your project. This is particularly useful when working with multiple branches to prevent migration conflicts during merges.

## Purpose

When multiple developers work on different features in separate branches that require database migrations, they might unknowingly create migrations with the same number. This can lead to conflicts when merging branches. This script helps identify such conflicts early in the development process.

## Installation

Clone the repository:
```bash
git clone https://github.com/samiashi/django-migration-checker.git
cd django-migration-checker
```

## Usage

Run the script from your Django project's root directory:
```bash
python migration_checker.py
```

### Sample Output

When duplicates are found:
```
🔴 Duplicate Migration Numbers Found:

[app_name]
  Migration #3:
    - 0003_alter_field.py
    - 0003_add_new_model.py

❌ Found conflicting migration numbers!
Please renumber your migrations to avoid conflicts.
```

When no duplicates are found:
```
✅ No duplicate migration numbers found!
```

## GitHub Actions Integration

You can use this script in your CI/CD pipeline to automatically check for migration conflicts. Here's an example GitHub Actions workflow:

```yaml
name: Check Migration Numbers

on: [pull_request]

jobs:
  check-migrations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Check for duplicate migrations
        run: python migration_checker.py
```

## Features

- Recursively scans all Django apps in your project
- Identifies duplicate migration numbers within each app
- Provides clear, formatted output of conflicts
- Returns non-zero exit code when duplicates are found (useful for CI/CD)
- Type-annotated Python code

## Requirements

- Python >= 3.10
- Django project structure with migrations
