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

