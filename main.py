from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Account
from schemas import AccountCreate, AccountOut, AmountIn, TransferIn, TransferOut
from services import deposit, withdraw, transfer


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    account = Account(owner_name=data.owner_name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@app.get("/accounts/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account 
@app.post("/accounts/{account_id}/deposit", response_model=AccountOut)
def deposit_endpoint(account_id: int, data: AmountIn, db: Session = Depends(get_db)):
    return deposit(db, account_id, data.amount_cents)


@app.post("/accounts/{account_id}/withdraw", response_model=AccountOut)
def withdraw_endpoint(account_id: int, data: AmountIn, db: Session = Depends(get_db)):
    return withdraw(db, account_id, data.amount_cents)


@app.post("/transfers", response_model=TransferOut)
def transfer_endpoint(data: TransferIn, db: Session = Depends(get_db)):
    sender, receiver = transfer(db, data.from_id, data.to_id, data.amount_cents)
    return {"sender": sender, "receiver": receiver}