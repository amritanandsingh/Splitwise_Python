# Expense Management System

## Overview

This Expense Management System is a FastAPI application designed to help users manage and track expenses among a group. The system allows users to add expenses, view their balances, and sends email notifications for expense updates.


## Database Schema

The application uses a relational database with the following schema:

- `User`
  - `userid` (primary key)
  - `name`
  - `email`
  - `phonenumber`

- `Expense`
  - `expenseId` (primary key)
  - `userid` (foreign key to User)
  - `amount`
  - `type` (Exact or Percent)
  - `expenseName`
  - `notes`
  - `createdAt`
  - `participants` (List of Participants)

- `Balance`
  - `userid` (foreign key to User)
  - `BalancesForEveryone` (List of Participants)

## Classes and Interfaces

### User

```python
class User(BaseModel):
    userid: str
    name: str
    email: EmailStr
    phonenumber: Optional[str] = None
```

### Expense

```python
class Expense(BaseModel):
    expenseId: str
    userid: str
    amount: float
    type: str
    expenseName: Optional[str] = None
    notes: Optional[str] = None
    createdAt: str = None
    participants: List[Participant]
```

### Balance

```python
class Balance(BaseModel):
    userid: str
    BalancesForEveryone: List[Participant]
```

### Participant

```python
class Participant(BaseModel):
    userid: str
    share: float
```

## API Endpoints

### Users

- `GET /api/user/all`: Get all users.
- `POST /api/user/add`: Add a new user.

### Expenses

- `GET /api/expense/all`: Get all expenses and balances.
- `POST /api/expense/add`: Add a new expense.
- `GET /api/expense/user`: Get expenses for a specific user.
- `GET /api/expense/user/carryoff`: Get users with non-zero balance.

### Email

- `POST /api/email`: Send email notifications.

## How to Run

1. Clone the repository.
2. Install dependencies (`pip install -r requirements.txt`).
3. Configure the application settings.
4. Run the FastAPI application (`uvicorn app:app --reload`).

