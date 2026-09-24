from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Account


def deposit(db: Session, account_id: int, amount_cents: int):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance_cents += amount_cents
    db.commit()
    db.refresh(account)
    return account

def withdraw(db: Session, account_id: int, amount_cents: int):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    if amount_cents > account.balance_cents:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account.balance_cents -= amount_cents
    db.commit()
    db.refresh(account)
    return account

def transfer(db: Session, from_id: int, to_id: int, amount_cents: int):
    sender = db.get(Account, from_id)
    receiver = db.get(Account, to_id)

    if sender is None or receiver is None:
        raise HTTPException(status_code=404, detail="Account not found")

    if amount_cents > sender.balance_cents:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    try:
        sender.balance_cents -= amount_cents
        receiver.balance_cents += amount_cents
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(sender)
    db.refresh(receiver)
    return sender, receiver