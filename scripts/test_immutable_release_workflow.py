#!/usr/bin/env python3
"""Fail-closed release-policy and raw-JAR tests for Gastronomicon."""
import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile

from verify_immutable_release_jar import verify

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/build.yml"
INSTALLER = ROOT / "scripts/install_maven_3_10.sh"


def verify_workflow_policy(source: str) -> None:
    raw_name = "name: " + chr(36) + "{{ env.OUTPUT_NAME }}"
    required = (
        "github.event_name == 'push' && github.ref == 'refs/heads/master'",
        'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"',
        'git/ref/heads/master" --jq',
        'test "$JAR" = "$SOURCE"',
        "python3 scripts/verify_immutable_release_jar.py",
        raw_name,
        "archive: false",
        "releases/tags/$TAG",
        "git/ref/tags/$TAG",
        "HTTP 404",
        'gh api --method POST "repos/$GITHUB_REPOSITORY/git/refs"',
        'gh release create "$TAG" "$SOURCE" --verify-tag',
        'gh release download "$TAG" --repo "$GITHUB_REPOSITORY"',
        'docs/releases/$RELEASE_VERSION.md',
        'if max_major == 0 or max_major > 65:',
        "26.3.build.230-stable",
    )
    for item in required:
        if item not in source:
            raise ValueError("Missing immutable publisher requirement: " + item)
    if source.count("python3 scripts/verify_immutable_release_jar.py") != 3:
        raise ValueError("Raw JAR must be checked during staging, before tag creation and after official download")
    if source.index("releases/tags/$TAG") > source.index('gh release create "$TAG"'):
        raise ValueError("Must reject existing release before tag creation")
    if source.index("git/ref/tags/$TAG") > source.index('gh release create "$TAG"'):
        raise ValueError("Must refuse orphan tag before release creation")
    for forbidden in ("--clobber", "gh release upload", "gh release edit",
                      "gh release delete", "git push --force", "git tag -f"):
        if forbidden in source:
            raise ValueError("Forbidden immutable release mutation: " + forbidden)
    if "if: github.event_name == 'workflow_dispatch' ||" in source:
        raise ValueError("Manual/branch workflow is not a verified master release")


class ImmutableWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_current_immutable_policy(self):
        verify_workflow_policy(self.source)

    def test_old_clobber_path_rejected(self):
        with self.assertRaises(ValueError):
            verify_workflow_policy(self.source.replace(
                'gh release create "$TAG" "$SOURCE" --verify-tag',
                'gh release upload "$TAG" "$SOURCE" --clobber', 1))

    def test_manual_dispatch_cannot_publish(self):
        with self.assertRaises(ValueError):
            verify_workflow_policy(self.source.replace(
                "github.event_name == 'push' && github.ref == 'refs/heads/master'",
                "github.event_name == 'workflow_dispatch'", 1))

    def test_source_sha_cannot_be_omitted(self):
        with self.assertRaises(ValueError):
            verify_workflow_policy(self.source.replace(
                'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"', "true", 1))

    def test_existing_tag_cannot_be_ignored(self):
        with self.assertRaises(ValueError):
            verify_workflow_policy(self.source.replace(
                "git/ref/tags/$TAG", "git/ref/heads/fake", 1))

    def test_official_asset_must_be_downloaded(self):
        with self.assertRaises(ValueError):
            verify_workflow_policy(self.source.replace(
                'gh release download "$TAG" --repo "$GITHUB_REPOSITORY"',
                "echo imaginary release", 1))

    def test_maven_archive_remains_checksum_verified(self):
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("archive.apache.org/dist/maven/maven-3", script)
        self.assertIn("sha512sum --check --status", script)
        self.assertIn("908b1501bfb420bf7c8affb855534a9c", script)


class RawJarVerificationTest(unittest.TestCase):
    @staticmethod
    def create(root: Path, major: int = 65) -> Path:
        jar = root / "SF_Gastronomicon1.1.5.jar"
        header = b"\xca\xfe\xba\xbe\x00\x00" + major.to_bytes(2, "big")
        with zipfile.ZipFile(jar, "w") as z:
            z.writestr("plugin.yml",
                "name: Gastronomicon\nversion: 1.1.5\n"
                "main: io.github.schntgaispock.gastronomicon.Gastronomicon\n")
            z.writestr("io/github/schntgaispock/gastronomicon/Gastronomicon.class", header)
        return jar

    def test_good_synthetic_jar(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = self.create(Path(tmp))
            verify(jar, "1.1.5", hashlib.sha256(jar.read_bytes()).hexdigest())

    def test_wrong_digest_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = self.create(Path(tmp))
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                verify(jar, "1.1.5", "0" * 64)

    def test_java_newer_than_21_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = self.create(Path(tmp), major=69)
            with self.assertRaisesRegex(ValueError, "exceeds Java 21"):
                verify(jar, "1.1.5", hashlib.sha256(jar.read_bytes()).hexdigest())

    def test_existing_version_cannot_be_reassigned(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = self.create(Path(tmp))
            with self.assertRaises(ValueError):
                verify(jar, "1.1.6", hashlib.sha256(jar.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
