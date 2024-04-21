# Wallet Transaction System

Create a wallet transaction system, like Paytm

[Problem Statement](./problem_statement.pdf)


## Setup

`docker-compose up`

This should run the app on port 1970

## Health Check

`curl --location 'http://127.0.0.1:1970/ping'`

should return `pong`

## Test


`docker-compose run test pytest --cov=app`


## Usage

> 1. Create user

```bash
curl --location 'http://127.0.0.1:1970/user' \
--header 'Content-Type: application/json' \
--data '{
    "phone": "1234567890"
}'
```


**Response**

```json
{
    "message": "User created successfully",
    "user": {
        "id": 3,
        "phone": "1234567890"
    }
}
```

> 2. Create wallet

```bash
curl --location 'http://127.0.0.1:1970/wallet' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 1,
    "wallet_type": "standard"
}'
```

**Response**

```json
{
    "wallet_id": 1
}
```

> 3. Check wallet balance


```bash
curl --location 'http://127.0.0.1:1970/wallet/1'
```

**Response**

```json
{
    "balance": 0.0
}
```


> 4. Credit to wallet

```bash
curl --location 'http://127.0.0.1:1970/wallet/1/credit' \
--header 'Content-Type: application/json' \
--data '{
    "amount": 10000
}'
```

**Response**

```json
{
    "message": "Wallet credited successfully"
}
```

> 5. Debit from wallet

```bash
curl --location 'http://127.0.0.1:1970/wallet/1/debit' \
--header 'Content-Type: application/json' \
--data '{
    "amount": 300
}'
```

**Response**


```json
{
    "message": "Wallet debited successfully"
}
```


> 6. View Transactions

```bash
curl --location --request GET 'http://127.0.0.1:1970/wallet/1/transactions' \
--header 'Content-Type: application/json' \
--data '{
    "amount": 300
}'
```

**Response**

```json
{
    "transactions": [
        {
            "amount": 10000.0,
            "id": 1,
            "timestamp": "Sun, 21 Apr 2024 22:11:31 GMT",
            "transaction_type": "credit"
        },
        {
            "amount": 300.0,
            "id": 2,
            "timestamp": "Sun, 21 Apr 2024 22:12:37 GMT",
            "transaction_type": "debit"
        },
        {
            "amount": 1400.0,
            "id": 3,
            "timestamp": "Sun, 21 Apr 2024 22:16:11 GMT",
            "transaction_type": "credit"
        }
    ]
}
```
