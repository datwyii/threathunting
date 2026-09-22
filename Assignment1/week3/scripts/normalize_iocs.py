"""Starter IOC normalization script for Week 3.

This script reads raw IOC data, applies simple cleaning/validation rules,
and writes normalized results for later import into MISP.
"""

from __future__ import annotations

import csv
import hashlib
import ipaddress
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw_iocs.csv"
NORMALIZED_FILE = BASE_DIR / "data" / "normalized_iocs.csv"


def is_valid_ipv4(value: str) -> bool:
    """Return True if value is a valid IPv4 address."""
    try:
        ip_obj = ipaddress.ip_address(value)
    except ValueError:
        return False
    return ip_obj.version == 4


def is_valid_sha256(value: str) -> bool:
    """Return True if value looks like a SHA256 hash."""
    if len(value) != 64:
        return False

    # hashlib can validate hexadecimal encoding by attempting to decode it.
    try:
        hashlib.new("sha256", bytes.fromhex(value))
    except ValueError:
        return False
    return True


def normalize_value(ioc_type: str, value: str) -> str | None:
    """Clean and validate IOC value by type.

    Returns normalized value, or None when the value is not valid.
    """
    cleaned = value.strip()

    if ioc_type == "domain":
        # Domains should be compared case-insensitively, so lowercase them.
        return cleaned.lower() if cleaned else None

    if ioc_type == "ip":
        return cleaned if is_valid_ipv4(cleaned) else None

    if ioc_type == "sha256":
        # Hash values are usually represented in lowercase.
        cleaned = cleaned.lower()
        return cleaned if is_valid_sha256(cleaned) else None

    # For other IOC types (e.g., url), keep trimmed value.
    return cleaned if cleaned else None


def main() -> None:
    """Read raw IOC rows, clean them, and write normalized rows."""
    processed = 0
    removed = 0
    normalized_rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    with RAW_FILE.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            processed += 1

            ioc_type = (row.get("type") or "").strip().lower()
            value = (row.get("value") or "").strip()
            source = (row.get("source") or "").strip()

            # Remove empty rows or rows missing key fields.
            if not ioc_type and not value and not source:
                removed += 1
                continue
            if not ioc_type or not value:
                removed += 1
                continue

            normalized_value = normalize_value(ioc_type, value)
            if normalized_value is None:
                removed += 1
                continue

            normalized_row = {
                "type": ioc_type,
                "value": normalized_value,
                "source": source,
            }
            row_key = (
                normalized_row["type"],
                normalized_row["value"],
                normalized_row["source"],
            )

            # Remove duplicates after normalization.
            if row_key in seen:
                removed += 1
                continue

            seen.add(row_key)
            normalized_rows.append(normalized_row)

    with NORMALIZED_FILE.open("w", encoding="utf-8", newline="") as outfile:
        fieldnames = ["type", "value", "source"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_rows)

    kept = len(normalized_rows)
    print(f"Processed records: {processed}")
    print(f"Removed records: {removed}")
    print(f"Kept records: {kept}")


if __name__ == "__main__":
    main()
