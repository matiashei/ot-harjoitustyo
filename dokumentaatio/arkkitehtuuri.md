# Pakkauskaavio

```mermaid
flowchart TD

A[UI] --> B[Services]
B --> C[Repositories]
C --> E[Database]
C --> D[Entities]
B --> D
```

## Sovelluslogiikka

Sovelluksen loogisen tietomallin muodostavat luokat [User](https://github.com/matiashei/ot-harjoitustyo/blob/main/tilix-app/src/entities/user.py), [Account](https://github.com/matiashei/ot-harjoitustyo/blob/main/tilix-app/src/entities/account.py) ja [Transaction](https://github.com/matiashei/ot-harjoitustyo/blob/main/tilix-app/src/entities/transaction.py).

```mermaid
classDiagram
    Transaction --> Account
    Account --> User 
    class User {
        -id: int
        -username: str
        -password_hash: str
    }

    class Account {
        -id: int
        -name: str
        -balance: float
        -user_id: int
    }

    class Transaction {
        -id: int
        -amount: float
        -date: datetime
        -description: str
        -account_id: int
    }
```
