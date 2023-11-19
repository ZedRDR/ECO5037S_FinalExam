# This was the initial script used to create the escrow account.
# The escrow account is being used to funds accounts in the other scripts to avoid manual dispensing
# Do not run this script. The first output, which is the account address and private key has been hardcoded on the other scripts

from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod

# Initialize Algod client for Algonode TestNet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address)

# example: ACCOUNT_GENERATE
private_key, address = account.generate_account()
print(f"address: {address}")
print(f"private key: {private_key}")
print(f"mnemonic: {mnemonic.from_private_key(private_key)}")
# example: ACCOUNT_GENERATE

