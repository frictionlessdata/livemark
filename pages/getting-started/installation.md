# Installation

```yaml remark
type: danger
text: Livemark executes code in documents that you build. It means that you MUST never build/start any Livemark projects from untrusted sources. Treat any Livemark project as you treat Python or Bash scripts security-wise
```

Livemark is a Python library that works on Windown, MacOs, and Linux. It uses SemVer for semantic versioning. Please file an [issue](https://github.com/frictionlessdata/livemark/issues) if you run into any problems during installation.

## Install

Livemark can be installed with pip (or [pipx](https://pypa.github.io/pipx/)):

```bash
$ pip install livemark
```

After installation, you can start writing your document (eg an `index.md` file) using the extended Markdown syntax described in the next sections.

## Verify

To make sure that Livemark is installed correctly on your machine:

```bash
$ livemark --version
```
```
1.0.0
```
