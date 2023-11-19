import algokit 
import algokit_utils as algokit

from typing import Dict, Any
import json
from base64 import b64decode


import algosdk as algosdk
from algosdk.v2client import algod
from algosdk import account, transaction
from pprint import pprint

def main():
    # Initialize Algod client for Algonode TestNet
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    algod_client = algod.AlgodClient(algod_token, algod_address)

    #####################################################################
    # Create accounts for buyer and seller
    #####################################################################
    # Each account must have a minimum of 200,000 micro Algos to transact

    # Fetch account info of a predefined account (example)
    accountE = '4J22EFWCMWEDRK4MTEFUXWD5WQ5ZSPMI5LROSYOIBHBISXIUPQVOJLB5FA'
    try:
        account_info = algod_client.account_info(accountE)
        print(f"Escrow Account balance: {account_info.get('amount')} microAlgos")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Generate 2 new accounts
    # Generate Account B for Seller of NFT
    accountB = algokit.Account.new_account()
    print("Seller address: ", accountB.address)

    # Generate Account A for Buyer of NFT
    accountA = algokit.Account.new_account()
    print("Buyer address: ", accountA.address)

    #####################################################################
    # Fund the buyer and sellers accounts from escrow account
    #####################################################################

    # Top up buyer
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=accountE,
        sp=params,
        receiver=accountA.address,
        amt=5202000,
        note=b"Top up Buyer",
    )

    signed_txn = unsigned_txn.sign('+ISj6hwhHxlHzv5b32Ww8FmYhlQUvqrJZaggp5FPifzidaIWwmWIOKuMmQtL2H20O5k9iOri6WHICcKJXRR8Kg==')

    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

    # Add here the logic to fund the new account using your prefunded account
    # This typically involves creating and sending a transaction

# Top up seller
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=accountE,
        sp=params,
        receiver=accountB.address,
        amt=202000,
        note=b"Top up Seller",
    )

    signed_txn = unsigned_txn.sign('+ISj6hwhHxlHzv5b32Ww8FmYhlQUvqrJZaggp5FPifzidaIWwmWIOKuMmQtL2H20O5k9iOri6WHICcKJXRR8Kg==')

    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

    # Add here the logic to fund the new account using your prefunded account
    # This typically involves creating and sending a transaction

    #Display ballances

    account_info = algod_client.account_info(accountE)
    print(f"Escrow Account balance: {account_info.get('amount')} microAlgos")
    
    account_info = algod_client.account_info(accountA.address)
    print(f"Buyer Account balance: {account_info.get('amount')} microAlgos")
    
    account_info = algod_client.account_info(accountB.address)
    print(f"Seller Account balance: {account_info.get('amount')} microAlgos")


    #####################################################################
    # Create ASA for seller
    #####################################################################

   # accountB (Seller) create 2 ASA (Algorand Standard Asset, token, asset, NFT, etc.)
    unsigned_tx = algosdk.transaction.AssetCreateTxn(
        sender=accountB.address,
        sp=algod_client.suggested_params(),
        total=2,
        decimals=0,
        default_frozen=False
    )

    # sign transaction
    signed_txn = unsigned_tx.sign(accountB.private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    try:
        txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)
        results = algod_client.pending_transaction_info(txid)
        assetID = results.get("asset-index")  # Use .get() to avoid KeyError
        if assetID is not None:
            print("assetID: ", assetID)
        else:
            print("Asset index not found in the transaction information.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # get info about accountB from algod
    pprint(algod_client.account_info(accountB.address))

    # print the assetID of my new asset from algod
    results = algod_client.pending_transaction_info(txid)
    assetID = results["asset-index"]
    print("assetID: ", assetID) 

    # Buyer opts into the ASA
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender=accountA.address,
        sp=algod_client.suggested_params(),
        receiver=accountA.address,
        amt=0,
        index=assetID,
    )

    signed_txn = unsigned_txn.sign(accountA.private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (opt-in to ASA): {}".format(txid))

    #####################################################################
    # Atomic Transfer between Account A and Account B
    #####################################################################

    # Account A sends 5 Algo to Account B
    payment_txn_A = algosdk.transaction.PaymentTxn(
        sender=accountA.address,
        sp=algod_client.suggested_params(),
        receiver=accountB.address,
        amt=5_000_000
    )

    # Account B sends 2 ASA to Account A
    transfer_txn_B = algosdk.transaction.AssetTransferTxn(
        sender=accountB.address,
        sp=algod_client.suggested_params(),
        receiver=accountA.address,
        amt=2,
        index=assetID,
    )

    # Group the transactions
    group_id = algosdk.transaction.calculate_group_id([payment_txn_A, transfer_txn_B])
    payment_txn_A.group = group_id
    transfer_txn_B.group = group_id

    # Sign the transactions
    signed_txn_A = payment_txn_A.sign(accountA.private_key)
    signed_txn_B = transfer_txn_B.sign(accountB.private_key)

    # Submit the atomic group
    txid = algod_client.send_transactions([signed_txn_A, signed_txn_B])
    print("Transaction ID (atomic transfer): {}".format(txid))

    # Wait for the atomic transfer to be confirmed
    try:
        # Wait for the transaction to be confirmed
        txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

        # After confirmation, get the pending transaction information
        results = algod_client.pending_transaction_info(txid)

        # Extract the asset ID, if available
        assetID = results.get("asset-index")  # Use .get() to avoid KeyError
        if assetID is not None:
            print("assetID: ", assetID)
        else:
            print("Asset index not found in the transaction information.")
    except Exception as e:
        print(f"An error occurred: {e}")

    pprint(algod_client.account_info(accountA.address))
    pprint(algod_client.account_info(accountB.address))

    def print_asset_holders(algod_client, asset_id, account_addresses):
        for address in account_addresses:
            account_info = algod_client.account_info(address)
            assets = account_info.get('assets', [])
            for asset in assets:
                if asset['asset-id'] == asset_id:
                    print(f"Account {address} holds {asset['amount']} of asset {asset_id}")


    print_asset_holders(algod_client, assetID, [accountA.address, accountB.address])


    print("Final result:")

    account_info = algod_client.account_info(accountA.address)
    print(f"Buyer Account balance: {account_info.get('amount')} microAlgos")
    
    account_info = algod_client.account_info(accountB.address)
    print(f"Seller Account balance: {account_info.get('amount')} microAlgos")

    print(f"The ASA with ID {assetID} is now owned by the seller.")

if __name__ == "__main__":
    main()

