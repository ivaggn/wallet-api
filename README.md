# Wallet API

[One or two sentences: what it does, and what it's built with]

## Features
- Create accounts
- Deposit and withdraw funds
- Transfer funds between accounts
- [anything else you think is worth mentioning]

## Tech stack
- Python, FastAPI
- SQLAlchemy, SQLite
- Pytest

## Setup
\`\`\`
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Running tests
\`\`\`
pytest
\`\`\`

## API endpoints
- POST /accounts
- GET /accounts/{account_id}
- POST /accounts/{account_id}/deposit
- POST /accounts/{account_id}/withdraw
- POST /transfers
