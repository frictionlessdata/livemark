# Python Development

Livemark can be used in software development as a helper tool for working on Python projects. It provides an ability to create documentation sites and works as a task runner.

## Example

Livemark's documentation site is written in Livemark:

> https://livemark.frictionlessdata.io/

```yaml image
path: ../../assets/example.png
width: 100%
height: unset
class: border
```

## Prerequisites

Create a virtual environment (optional):

```bash
$ python3 -m venv .python
$ source .python/bin/activate
```

And install livemark:

```
$ pip install livemark
```

## Writing Docs

Working on a documentation site is not really different to working on a regular Livemark project. The main difference will be having your documentation along side with the codebase itself.

First of all, create:
- `livemark.yaml`
- `index.md`
- `pages/contrib.md` (for example)

Fill in your configuration file:

> livemark.yaml

```yaml
brand:
  text: My Project
about:
  text: My project is a software
site:
  favicon: assets/favicon.ico
github:
  user: <user>
  repo: <repo>
topics:
  selector: h2
links:
  items:
    - name: About Me
      path: https://personal.site
pages:
  items:
    - name: Introduction
      path: index
    - path: pages/contrib
```

Run a livereload server locally:

```bash
$ livemark start
```

When you are ready to publish your work, commit the changes and push it to Github. The only missing part now is enabling Github Pages:

> https://guides.github.com/features/pages/

```yaml image
path: ../../assets/deploy.png
width: 75%
height: unset
class: border
```

After this step your documentation portal will be up and running.

## Getting Tests

> A special Livemark command for testing docs is under construction

An important thing about Livemark is that it runs scripts in documents during processing. It means that it basically tests all your code snippets on every build.

For example, our guide includes this code (with a built output):

> guide.md

```
'''python script
mylib.command('Hello World')
'''
'''
Hello World
'''
```

Every time during the build the software will be tested.

## Running Tasks

Livemark supports having tasks written in Markdown documents. For example, if we have a `contrib.md` section like this, we need to add this page to `livemark.yaml:pages.items` to make it work:

> contrib.md

```
'''bash task id=test-lint
echo 'Test Lint'
'''
'''python task id=test-code
print('Test Code')
'''
```

Use this command to get a list of available tasks:

```bash
$ livemark run
```
```
test-lint
test-code
```

Execute all of the tests:

```bash
$ livemark run test
```
```
Test Link
Test Code
```

Or run an arbitrary task:

```bash
$ livemark run test-code
```
```
Test Code
```
