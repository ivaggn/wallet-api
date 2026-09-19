from pydantic import BaseModel, ConfigDict, Field


class AccountCreate(BaseModel):
	owner_name: str = Field(min_length=1)


class AccountOut(BaseModel):
	id: int
	owner_name: str
	balance_cents: int

	model_config = ConfigDict(from_attributes=True)