from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
	owner_name: str = Field(min_length=1)


class AccountOut(BaseModel):
	id: int
	owner_name: str
	balance_cents: int

	model_config = ConfigDict(from_attributes=True)

class AmountIn(BaseModel):
    amount_cents: int = Field(gt=0)


class TransferIn(BaseModel):
    from_id: int
    to_id: int
    amount_cents: int = Field(gt=0)


class TransferOut(BaseModel):
    sender: AccountOut
    receiver: AccountOut