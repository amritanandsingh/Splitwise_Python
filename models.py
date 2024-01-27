from pydantic import BaseModel, EmailStr
from typing import Optional, List

class User(BaseModel):
    userid: str
    name: str
    email: EmailStr
    phonenumber: Optional[str] = None

class Participant(BaseModel):
    userid: str
    share: float
    
class Expense(BaseModel):
    expenseId: str
    userid: str
    amount: float
    type: str  # Exact or Percent 
    expenseName: Optional[str] = None
    notes: Optional[str] = None
    createdAt: str  
    participants: List[Participant]

class Balance(BaseModel):
    userid: str
    BalancesForEveryone: List[Participant]







