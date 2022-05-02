# print-and-play

[![Verify](https://github.com/marqueewinq/steesh/actions/workflows/verify.yml/badge.svg)](https://github.com/marqueewinq/steesh/actions/workflows/verify.yml)

CSV to printable pdf converter

## Development

### Setup

1. Activate virtualenv:
```bash
virtualenv env --python=python3.9
source env/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```
3. Activate pre-commit hooks:
```bash
pre-commit install
```
4. You're all set! :rocket: Launch service locally with:

```bash
docker-compose up --build
```

### Tests

Launch unit tests with:

```bash
python -m pytest
```

For integration tests you'll need to install playwright and have an `docker-compose`
instance running:

```bash
playwright install
docker-compose up -d
python -m pytest --integration
```

### Render locally

Steesh comes with a simple Web UI; but you can use `steesh.renderer` package directly
with:

```bash
python -m steesh --help
```
