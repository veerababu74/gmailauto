#!/usr/bin/env python3
"""
Convert all remaining Pydantic v2 syntax to v1 for full compatibility
"""
import os
import re


def convert_pydantic_v2_to_v1_complete(file_path):
    """Convert all Pydantic v2 syntax to v1 syntax"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Replace field_validator with validator
    content = re.sub(r"field_validator", "validator", content)

    # Replace mode="before" with pre=True
    content = re.sub(r'mode="before"', "pre=True", content)

    # Remove @classmethod decorator from validators
    content = re.sub(
        r"@validator\([^)]+\)\s*@classmethod\s*def",
        r"@validator\g<1>\n    def",
        content,
    )

    # Replace pydantic_settings import
    content = re.sub(
        r"from pydantic_settings import BaseSettings",
        "from pydantic import BaseSettings",
        content,
    )

    # Replace from_attributes with orm_mode
    content = re.sub(r"from_attributes\s*=\s*True", "orm_mode = True", content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Updated {file_path}")
        return True
    else:
        print(f"- No changes needed in {file_path}")
        return False


def scan_and_convert():
    """Scan all Python files and convert Pydantic v2 to v1"""
    updated_files = []

    for root, dirs, files in os.walk("app"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if convert_pydantic_v2_to_v1_complete(file_path):
                    updated_files.append(file_path)

    # Also check main files
    for file in ["main.py", "database.py"]:
        if os.path.exists(file):
            if convert_pydantic_v2_to_v1_complete(file):
                updated_files.append(file)

    return updated_files


if __name__ == "__main__":
    print("🔄 Converting all Pydantic v2 syntax to v1...")
    updated_files = scan_and_convert()

    if updated_files:
        print(f"\n✅ Converted {len(updated_files)} files:")
        for file_path in updated_files:
            print(f"  - {file_path}")
    else:
        print("\n✅ All files already use Pydantic v1 syntax")

    print("\n🎯 Ready for deployment with Pydantic v1!")
