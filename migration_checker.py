import logging
import os
import re
from collections import defaultdict

logger = logging.getLogger(__name__)


def get_migration_number(filename: str) -> int | None:
    match = re.match(r"^(\d{4})_.*\.py$", filename)
    return int(match.group(1)) if match else None


def check_migrations() -> tuple[bool, dict[str, list[tuple[int, list[str]]]]]:
    """
    Check for duplicate migration numbers across all Django apps.

    Returns:
        Tuple containing:
        - Boolean indicating if duplicates were found
        - Dict of app_name -> list of (number, filenames) for duplicates
    """
    has_duplicates = False
    duplicate_report = defaultdict(list)

    # Get all Django apps with migrations
    for root, dirs, files in os.walk("."):
        if "migrations" not in dirs:
            continue

        migration_path = os.path.join(root, "migrations")
        app_name = os.path.basename(root)

        if not os.path.isdir(migration_path):
            continue

        # Get all migration files
        migration_files = [
            f
            for f in os.listdir(migration_path)
            if f.endswith(".py") and not f.startswith("__")
        ]

        # Sort migration files by number
        migration_files.sort(key=lambda x: get_migration_number(x) or -1)

        # Track numbers for this app
        numbers = defaultdict(list)

        for filename in migration_files:
            if number := get_migration_number(filename):
                numbers[number].append(filename)

        # Check for duplicates
        for number, filenames in sorted(numbers.items()):
            if len(filenames) > 1:
                has_duplicates = True
                duplicate_report[app_name].append((number, filenames))

    return has_duplicates, duplicate_report


def print_report(duplicate_report: dict[str, list[tuple[int, list[str]]]]) -> None:
    if not duplicate_report:
        return

    logger.warning("\n🔴 Duplicate Migration Numbers Found:")

    for app_name, duplicates in sorted(duplicate_report.items()):
        logger.warning(f"\n[{app_name}]")
        for number, filenames in sorted(duplicates, key=lambda x: x[0]):
            logger.warning(f"  Migration #{number}:")
            for fname in filenames:
                logger.warning(f"    - {fname}")


def main() -> None:
    has_duplicates, duplicate_report = check_migrations()

    if has_duplicates:
        print_report(duplicate_report)
        logger.error("\n❌ Found conflicting migration numbers!")
        logger.error("Please renumber your migrations to avoid conflicts.")
        exit(1)
    else:
        logger.info("\n✅ No duplicate migration numbers found!")


if __name__ == "__main__":
    """
    This script is used to check for duplicate migration numbers across all Django apps.
    It is used in the GitHub Actions workflow to check for duplicate migration numbers
    when a pull request is opened.

    This is to avoid conflicts when merging migrations from different branches.

    Returns something like:

    ```
    🔴 Duplicate Migration Numbers Found:

    [accounts]
        Migration #3:
            - 0003_add_user_fields.py
            - 0003_update_user_model.py

    [products]
        Migration #101:
            - 0101_add_product_category.py
            - 0101_product_pricing_fields.py

    ❌ Found conflicting migration numbers!
    Please renumber your migrations to avoid conflicts.
    ```

    OR

    ```
    ✅ No duplicate migration numbers found!
    ```
    """
    main()
