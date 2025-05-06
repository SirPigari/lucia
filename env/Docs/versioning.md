# Versioning
###### 6.5.2025

---

We use [Semantic Versioning](https://semver.org/) (SemVer) for versioning our releases. The version number follows the format `MAJOR.MINOR.PATCH`, where:

- **MAJOR** version is incremented when incompatible API changes are introduced.
- **MINOR** version is incremented when functionality is added in a backward-compatible manner.
- **PATCH** version is incremented when backward-compatible bug fixes are made.

---

## Versioning Scheme

### ✅ Release Version

The official and stable version of the software:

- **Format**: `X.Y.Z`
- **Example**: `2.1.0`, `1.0.5`
- Implies production-readiness and stability.

---

### 🚧 Pre-release Version

Versions that precede a stable release. Indicate a work-in-progress or testing phase.

- **Format**: `X.Y.Z<pre-release-tag>`
- **Types**:
  - **Alpha (`a`)** – Not feature-complete. Early testing.
    - Examples: `1.0.0a`, `1.0.0a1`
  - **Beta (`b`)** – Feature-complete but potentially buggy.
    - Examples: `1.0.0b`, `1.0.0b2`
  - **Release Candidate (`rc`)** – Stable and ready unless critical bugs are found.
    - Examples: `1.0.0rc`, `1.0.0rc3`

---

### 🧪 Development Version

Used for in-progress development.

- **Format**: `X.Y.Z.devN`
- **Example**: `2.0.0.dev3`
- Typically used in CI/CD pipelines and internal testing environments.

---

### 🔨 Build Metadata

Provides additional build information (not used for version precedence).

- **Format**: `X.Y.Z+<build-metadata>`
- **Example**: `1.0.0+20130313144700`
- Often used to track exact builds in CI, like Git commit hashes or timestamps.

---

### 🔁 Rust Edition

Indicates the version is implemented in Rust.

- **Format**: `X.Y.Z-rust` or `X.Y.Zr`
- **Examples**: `1.2.0-rust`, `2.0.1r`
- Used to distinguish multi-language implementations.

---

### 🐍 Python Edition

Default version format without language-specific suffixes.

- **Format**: Any version lacking `-rust`, `r`, or similar suffix.
- **Examples**: `1.0.0`, `2.3.1b1`, `3.0.0rc`
- Assumed to be written in or compatible with Python.

---

## Migration Plan

A full transition from Python to Rust is planned for the next **major** release:

- **Target Version**: `2.0.0`
- All core functionality will be re-implemented in Rust to improve performance, memory safety, and concurrency.
- The `2.x.x` line will drop Python-based implementations and will focus exclusively on Rust.
- Backward compatibility will not be guaranteed in this release.
- Until version `2.0.0`, hybrid or dual-language support may continue using `-rust` and Python versions in parallel.

---

## Guidelines

- Increment **PATCH** for hotfixes or minor bug fixes.
- Increment **MINOR** for new features that do not break existing APIs.
- Increment **MAJOR** for breaking changes or large-scale refactors.
- Always move forward in version numbers; never reuse or "fix" a released version.
- Avoid skipping MAJOR versions unless justified by major platform or architecture shifts.

---
See [Changelog](../../README.md#changelog) for a detailed history of changes and updates.