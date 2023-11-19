# ECO5037S_FinalExam
Algorand Python scripts

# Algorand atomic transfer using Algokit
# Overview
This script showcases how to issue and distribute fractional NFTs (Non-Fungible Tokens) on the Algorand blockchain using Python. The script includes generating new accounts, creating a fractional NFT, distributing fractions of this NFT to different accounts, and verifying the ownership of these fractional NFTs.

# Features
Account Creation: Generates three new accounts in addition to an existing escrow account.
Funding Accounts: Utilizes a pre-funded escrow account to provide initial funds to the new accounts.
Fractional NFT Creation: Creates a fractional NFT (named "10 pieces of a cake") from the escrow account, which can be divided into ten parts.
NFT Distribution: Distributes parts of the fractional NFT to the three new accounts.
Ownership Verification: Checks and displays each account's ownership of the fractional NFT, indicating the number of units held or if an account holds no units.

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
1. Create and Fund New Accounts:
    Generates new accounts and funds them using the escrow account.
2. Create Fractional NFT:
    The escrow account creates a fractional NFT divisible into ten parts.
3. Distribute Fractional NFT:
    Distributes one-tenth of the NFT to each of the three new accounts.
4. Verify Ownership:
    Verifies and prints each account's holdings of the fractional NFT.

Output:
    The script outputs transaction details, account balances, and verifies the fractional NFT's distribution. It displays the ownership status of the NFT for each account.

# Output
The script outputs transaction details, account balances, and the final status of ASA ownership.
It verifies and prints the asset holders to confirm the successful transfer of the ASA.