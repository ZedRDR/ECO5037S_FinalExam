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
    accountE_privatekey = '+ISj6hwhHxlHzv5b32Ww8FmYhlQUvqrJZaggp5FPifzidaIWwmWIOKuMmQtL2H20O5k9iOri6WHICcKJXRR8Kg=='
    try:
        account_info = algod_client.account_info(accountE)
        print(f"Escrow Account balance: {account_info.get('amount')} microAlgos")
    except Exception as e:
        print(f"An error occurred: {e}")


    # Generate 3 new accounts
    
    # Generate Account B for Seller of NFT
    
    # Generate Account A for Buyer of NFT
    accountA = algokit.Account.new_account()
    print("Sizwe's address: ", accountA.address)
    
    accountB = algokit.Account.new_account()
    print("Bob's address: ", accountB.address)

    accountC = algokit.Account.new_account()
    print("Zaheer's address: ", accountC.address)


    #####################################################################
    # We have to fund the 3 new accounts so that they can cover the transaction cost
    # And have a minimum balance
    #####################################################################

    # Top up Sizwe, account A
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=accountE,
        sp=params,
        receiver=accountA.address,
        amt=202000,
        note=b"Top up account A"
    )

    signed_txn = unsigned_txn.sign('+ISj6hwhHxlHzv5b32Ww8FmYhlQUvqrJZaggp5FPifzidaIWwmWIOKuMmQtL2H20O5k9iOri6WHICcKJXRR8Kg==')

    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")


    # Top up Bob, account B
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=accountE,
        sp=params,
        receiver=accountB.address,
        amt=202000,
        note=b"Top up account B",
    )

    signed_txn = unsigned_txn.sign(accountE_privatekey)

    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")


    # Top up Zaheer, account C
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=accountE,
        sp=params,
        receiver=accountC.address,
        amt=202000,
        note=b"Top up account C",
    )

    signed_txn = unsigned_txn.sign(accountE_privatekey)

    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

    #Display ballances
    
    account_info = algod_client.account_info(accountA.address)
    print(f"Buyer Account balance: {account_info.get('amount')} microAlgos")
    
    account_info = algod_client.account_info(accountB.address)
    print(f"Seller Account balance: {account_info.get('amount')} microAlgos")

    account_info = algod_client.account_info(accountC.address)
    print(f"Escrow Account balance: {account_info.get('amount')} microAlgos")

    #####################################################################
    # Create ASA from the Escrow account
    #####################################################################

    # Escrow create 1 ASA (Algorand Standard Asset, token, asset, NFT, etc.)
    unsigned_tx = algosdk.transaction.AssetCreateTxn(
        sender=accountE,
        sp=algod_client.suggested_params(),
        total=10,
        decimals=1, #This is important and means that the ASA can be divided into 10 parts. Its fractional
        default_frozen=False,
        asset_name="10 pieces of a cake"
    )

    # sign transaction
    signed_txn = unsigned_tx.sign(accountE_privatekey)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    try:
        txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)
        results = algod_client.pending_transaction_info(txid)
        assetID = results.get("asset-index")  
        if assetID is not None:
            print("assetID: ", assetID)
        else:
            print("Asset index not found in the transaction information.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # get info about accountB from algod
    pprint(algod_client.account_info(accountE))

    # print the assetID of my new asset from algod
    results = algod_client.pending_transaction_info(txid)
    assetID = results["asset-index"]
    print("assetID: ", assetID) 

    #####################################################################
    # Other accounts opt-in to the NFT
    #####################################################################

    # Account A opts into the ASA
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

    # Account B opts into the ASA
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender=accountB.address,
        sp=algod_client.suggested_params(),
        receiver=accountB.address,
        amt=0,
        index=assetID,
    )

    signed_txn = unsigned_txn.sign(accountB.private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (opt-in to ASA): {}".format(txid))

    # Account C opts into the ASA
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
            sender=accountC.address,
            sp=algod_client.suggested_params(),
            receiver=accountC.address,
            amt=0,
            index=assetID,
        )

    signed_txn = unsigned_txn.sign(accountC.private_key)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (opt-in to ASA): {}".format(txid))            


    #####################################################################
    # Send fractional NFT
    #####################################################################

    # Send fractional NFT to Account A
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender=accountE,
        sp=algod_client.suggested_params(),
        receiver=accountA.address,
        amt=1,
        index=assetID
    )
    signed_txn = unsigned_txn.sign(accountE_privatekey)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (send fractional NFT to Account A): {}".format(txid))

    # Wait for confirmation 
    transaction.wait_for_confirmation(algod_client, txid, 4)

    # Send fractional NFT to Account B
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender=accountE,
        sp=algod_client.suggested_params(),
        receiver=accountB.address,
        amt=1,
        index=assetID
    )
    signed_txn = unsigned_txn.sign(accountE_privatekey)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (send fractional NFT to Account B): {}".format(txid))

    transaction.wait_for_confirmation(algod_client, txid, 4)

    # Send fractional NFT to Account C
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender=accountE,
        sp=algod_client.suggested_params(),
        receiver=accountC.address,
        amt=1,
        index=assetID
    )
    signed_txn = unsigned_txn.sign(accountE_privatekey)
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction ID (send fractional NFT to Account C): {}".format(txid))

    transaction.wait_for_confirmation(algod_client, txid, 4)

    #####################################################################
    # Display ownership of NFT
    #####################################################################

    def check_and_display_ownership(algod_client, accounts, asset_id):
        for account in accounts:
            try:
                account_info = algod_client.account_info(account)
                assets = account_info.get('assets', [])
                found = False
                for asset in assets:
                    if asset['asset-id'] == asset_id:
                        print(f"Account {account} holds {asset['amount']} of 10 units of asset {asset_id}")
                        found = True
                        break
                if not found:
                    print(f"Account {account} does not hold any units of asset {asset_id}")
            except Exception as e:
                print(f"An error occurred while fetching account info for {account}: {e}")

    asset_accounts = [accountA.address, accountB.address, accountC.address, accountE]
    check_and_display_ownership(algod_client, asset_accounts, assetID)

if __name__ == "__main__":
    main()

