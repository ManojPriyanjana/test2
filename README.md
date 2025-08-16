# Simple Web POS System

This repository contains a minimal point-of-sale system for a retail shop using HTML, CSS, JavaScript, and a SQLite database served through a small Python HTTP server.

## Features
- Display products from a SQLite database
- Add products to a cart and compute totals
- Checkout by sending cart data to the server

## Setup
Start the server:

```bash
python server.py
```

Then open `http://localhost:8000` in your browser to use the POS interface.

## Tests
Run unit tests with:

```bash
python -m unittest
```
