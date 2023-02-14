import os
import pdb

from algosdk.v2client import algod
from algosdk import mnemonic, account, constants, encoding, transaction


def opt_in(addr, private_key, asset_id):
    params = algod_client.suggested_params()

    txn = transaction.AssetTransferTxn(
        sender=addr, sp=params, receiver=addr, amt=0, index=asset_id
    )

    txn_signed = txn.sign(private_key.encode())
    txid = algod_client.send_transaction(txn_signed)
    transaction.wait_for_confirmation(algod_client, txid)


if __name__ == "__main__":
    algod_token = os.getenv("ALGOD_TOKEN")
    algod_address = os.getenv("ALGOD_ADDRESS")
    headers = {"X-API-Key": algod_token}

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    address = input("Enter the address of the account that will be opting in: ")
    account_mnemonic = input(
        "Enter the mnemonic of the account that will be opting in: "
    )
    private_key = mnemonic.to_private_key(account_mnemonic)
    asset_id = int(input("Enter the asset id: "))

    opt_in(address, private_key, asset_id)
    print("Opted in to asset id: " + str(asset_id))
