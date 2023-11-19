# ECO5037S_FinalExam
Algorand Python scripts

# Algorand atomic transfer using Algokit
# Overview
This script demonstrates an atomic transfer on the Algorand blockchain using Python. It includes the creation of two accounts (A and B), the creation of an Algorand Standard Asset (ASA), and the execution of an atomic transfer where Account A (Buyer) sends ALGO to Account B (seller), and Account B (seller) sends ASA units back to Account A (buyer).

# Features
Account Creation: Generate two new accounts (A and B) for the transaction.
Funding Accounts: Utilize a pre-funded escrow account to provide initial funds to both accounts.
ASA Creation: Account B creates an ASA.
Opt-in to ASA: Account A opts into the ASA created by Account B.
Atomic Transfer: Simultaneous transfer of ALGO from Account A to Account B and ASA units from Account B to Account A.

# Requirements
Python 3.x
Algorand SDK for Python (algosdk)
algokit and algokit_utils modules

# Setup
Install the Algorand SDK for Python.
Copy code
pip install py-algorand-sdk
Ensure algokit and algokit_utils are available in your Python environment.

# Usage
Run the script using Python in your terminal:
python atomic_transfer_script.py

# Script Details
A prefunded escrow account has been generated and funded with the Algorand Dispensor.
https://dispenser.testnet.aws.algodev.network/

Escrow Account (Pre-funded):
Address: 4J22EFWCMWEDRK4MTEFUXWD5WQ5ZSPMI5LROSYOIBHBISXIUPQVOJLB5FA
Private Key: +ISj6hwhHxlHzv5b32Ww8FmYhlQUvqrJZaggp5FPifzidaIWwmWIOKuMmQtL2H20O5k9iOri6WHICcKJXRR8Kg==
Mnemonic: (Not provided for security reasons)
This account is used to top up other accounts in the script.

# Transaction Flow
1. Create and Fund Account B:

Account B is generated and funded using the escrow account.
Account B creates an ASA.

2. Create and Fund Account A:
Account A is generated and funded.
Account A opts into the ASA created by Account B.

3. Execute Atomic Transfer:
Account A sends 5 Algo to Account B.
Account B sends 2 units of the ASA to Account A.
The transfer is atomic, ensuring both transactions occur simultaneously.

# Output
The script outputs transaction details, account balances, and the final status of ASA ownership.
It verifies and prints the asset holders to confirm the successful transfer of the ASA.