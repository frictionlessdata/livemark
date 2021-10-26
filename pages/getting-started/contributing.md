# Contributing

Livemark has been created by the Frictionless Data team and it's open for contributing for anyone who is interested. We're about to migrate this guide to using `livemark run` but, for now, you need to have `make` command installed or use underlaying command written in Makefile.

## Prepare

To start working on the project clone the repository and enter its directory:

```bash
$ git clone git@github.com:frictionlessdata/livemark.git
$ cd livemark
```

Create a virtual environment (optional):

```bash
$ python3 -m venv .python
$ source .python/bin/activate
```

And install dependencies:

```
$ make install
```

## Testing

With use Pytest for writing tests and Pylama for linting:

```bash
$ make test
```

## Releasing

Update the version in `livemark/assets/VERSION` and run:

```bash
$ make release
```
