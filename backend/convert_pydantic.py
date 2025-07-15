#!/usr/bin/env python3
"""
Convert Pydantic v2 syntax to v1 syntax for deployment compatibility
"""
import os
import re


def convert_pydantic_v2_to_v1(file_path):
    """Convert from_attributes = True to orm_mode = True"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace from_attributes = True with orm_mode = True
    updated_content = re.sub(r"from_attributes\s*=\s*True", "orm_mode = True", content)

    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"✓ Updated {file_path}")
        return True
    else:
        print(f"- No changes needed in {file_path}")
        return False


def main():
    schemas_dir = "app/schemas"
    if not os.path.exists(schemas_dir):
        print(f"Schemas directory not found: {schemas_dir}")
        return

    updated_files = []

    for filename in os.listdir(schemas_dir):
        if filename.endswith(".py"):
            file_path = os.path.join(schemas_dir, filename)
            if convert_pydantic_v2_to_v1(file_path):
                updated_files.append(file_path)

    if updated_files:
        print(f"\nConverted {len(updated_files)} files to Pydantic v1 syntax:")
        for file_path in updated_files:
            print(f"  - {file_path}")
    else:
        print("\nNo files needed conversion.")


if __name__ == "__main__":
    main()
