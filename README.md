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
curl --location 'http://127.0.0.1:1970/wallet/1/transactions?null=null&start_date=2020-06-21&end_date=2025-06-21'
```

**Response**

```json
{
    "transactions": [
        {
            "amount": 10000.0,
            "id": 1,
            "timestamp": "2024-04-21T22:11:31.995606",
            "transaction_type": "credit",
            "wallet_id": 1
        },
        {
            "amount": 300.0,
            "id": 2,
            "timestamp": "2024-04-21T22:12:37.804476",
            "transaction_type": "debit",
            "wallet_id": 1
        },
        {
            "amount": 1400.0,
            "id": 3,
            "timestamp": "2024-04-21T22:16:11.808685",
            "transaction_type": "credit",
            "wallet_id": 1
        },
        {
            "amount": 1400.0,
            "id": 4,
            "timestamp": "2024-04-21T22:28:12.668519",
            "transaction_type": "credit",
            "wallet_id": 1
        },
        {
            "amount": 1400.0,
            "id": 5,
            "timestamp": "2024-04-21T22:28:26.168124",
            "transaction_type": "credit",
            "wallet_id": 1
        },
        {
            "amount": 1400.0,
            "id": 6,
            "timestamp": "2024-04-21T22:28:26.951352",
            "transaction_type": "credit",
            "wallet_id": 1
        }
    ]
}
```
