#!/usr/bin/env python3
"""Fail-closed raw-JAR verification for new immutable Gastronomicon releases."""
import hashlib
from pathlib import Path
import re
import sys
import zipfile

MAIN = "io/github/schntgaispock/gastronomicon/Gastronomicon.class"
MAIN_DESCRIPTOR = "io.github.schntgaispock.gastronomicon.Gastronomicon"


def verify(path: Path, version: str, expected_sha256: str) -> None:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version):
        raise ValueError("Version must be an unmodified stable numeric release")
    if path.name != f"SF_Gastronomicon{version}.jar" or not path.is_file():
        raise ValueError("Canonical raw JAR name or file is missing")
    if not re.fullmatch("[0-9a-f]{64}", expected_sha256):
        raise ValueError("Missing expected raw-JAR SHA-256")
    with path.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
    if actual != expected_sha256:
        raise ValueError("Raw-JAR SHA-256 mismatch")
    with zipfile.ZipFile(path) as jar:
        if jar.testzip() is not None:
            raise ValueError("JAR ZIP entry failed CRC verification")
        names = set(jar.namelist())
        if not {"plugin.yml", MAIN}.issubset(names):
            raise ValueError("Gastronomicon main class or plugin.yml is absent")
        descriptor = jar.read("plugin.yml").decode("utf-8")
        for field, value in (("name", "Gastronomicon"), ("main", MAIN_DESCRIPTOR),
                             ("version", version)):
            if re.search(r"(?m)^" + re.escape(field) + r":\s*['\"]?"
                         + re.escape(value) + r"['\"]?\s*$", descriptor) is None:
                raise ValueError(f"Gastronomicon plugin.yml {field} mismatched")
        count = 0
        for entry in names:
            if not entry.endswith(".class"):
                continue
            data = jar.read(entry)[:8]
            if len(data) != 8 or data[:4] != b"\xca\xfe\xba\xbe":
                raise ValueError(f"Invalid Java class: {entry}")
            if int.from_bytes(data[6:8], "big") > 65:
                raise ValueError(f"Java class exceeds Java 21: {entry}")
            count += 1
        if count == 0:
            raise ValueError("No compiled Java classes")
    print(f"Verified {path.name}, {count} Java <=21 classes, sha256={actual}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: verify_immutable_release_jar.py JAR VERSION SHA256")
    try:
        verify(Path(sys.argv[1]), sys.argv[2], sys.argv[3])
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        raise SystemExit(f"FAIL Gastronomicon immutable release: {error}") from error
