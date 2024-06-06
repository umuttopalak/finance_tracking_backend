from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class FinancalItemType(str, Enum):
    income = "income"
    expense = "expense"
    
class Category(BaseModel):
    id: int
    name: str

class FinancialItem(BaseModel):
    id: int
    amount: float
    date: datetime
    category_id: int
    type: FinancalItemType
    description: str



