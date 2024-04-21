# Wallet Transaction System

## Requirements

Create a wallet transaction system, like Paytm, using Python programming language
(you are free to choose any web framework of your choice)

### Entities

- Wallet
- User (phone number of some unique identifier no additional fields required)

- Create relevant database tables in a SQLite database
Expose APIs for the following
- Create wallet for the user - there can be multiple wallet types, user can own
only 1 wallet of each type
- Credit money to the wallet
- Debit money from the wallet
- Get current balance for a user
- Retrieve the total amount credited and debited from a wallet within a specific time range

Points to note:

- Each wallet should have a minimum balance of X amount, any debit
transaction that makes the wallet balance less than X amount should not be
allowed.
- You should handle race conditions, where multiple debit transactions might be initiated on the same wallet.

Instructions for Submission
- Include a requirements.txt file listing any 3rd-party dependencies.
- Provide clear instructions in a README file for setting up and running the
system in a local environment.
- Share the code on GitHub or a similar platform.
- For bonus points, Dockerize the application.
