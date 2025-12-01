#!/bin/bash
set -e
pytest -q --disable-warnings --maxfail=1 --cov=backend/app --cov-report=term-missing
