from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class FinancalItemType(str, Enum):
    income = "income"
    expense = "expense"
    
class Category(BaseModel):
    id: str
    name: str
    
    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name
        }

class FinancialItem(BaseModel):
    id: str
    amount: float
    date: datetime
    category_id: str
    type: FinancalItemType
    description: str

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "category_id": self.category_id,
            "type": self.type.value,
            "description": self.description
        }



