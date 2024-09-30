from pydantic import BaseModel, Field
from typing import Optional

class Expense(BaseModel):
    amount: Optional[float] = Field(title="amount", description="The amount of the expense")
    sender: Optional[str] = Field(title="sender", description="The sender of the expense")
    receiver: Optional[str] = Field(title="receiver", description="The receiver of the expense")
    date: Optional[str] = Field(title="date", description="The date of the expense")