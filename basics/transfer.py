import os
import pdb

from algosdk.v2client import algod
from algosdk import mnemonic, account, constants, encoding, transaction


def to_microalgos(amount):
    return amount * 10**6


def transfer_algo(sender, receiver, pk, amount, note=""):
    sender_addr = sender["address"]

    # Get the suggested parameters from the node
    params = algod_client.suggested_params()

    txn = transaction.PaymentTxn(
        sender=sender_addr,
        sp=params,
        receiver=receiver,
        amt=amount,
        note=note,
    )

    stxn = txn.sign(pk)
    txid = algod_client.send_transaction(stxn)

    transaction.wait_for_confirmation(algod_client, txid)


def transfer_asset(sender, receiver, pk, asset_id, amount, note=""):
    sender_addr = sender["address"]

    # Get the suggested parameters from the node
    params = algod_client.suggested_params()

    txn = transaction.AssetTransferTxn(
        sender=sender_addr,
        sp=params,
        receiver=receiver,
        amt=amount,
        index=asset_id,
        note=note,
    )

    stxn = txn.sign(pk)
    txid = algod_client.send_transaction(stxn)

    transaction.wait_for_confirmation(algod_client, txid)


if __name__ == "__main__":
    algod_token = os.getenv("ALGOD_TOKEN")
    algod_address = os.getenv("ALGOD_ADDRESS")
    headers = {"X-API-Key": algod_token}

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    sender = {
        "address": os.getenv("SENDER_ADDRESS"),
        "mnemonic": os.getenv("SENDER_MNEMONIC"),
    }

    if algod_token is None:
        algo_token = input("Enter the algod token: ")

    if algod_address is None:
        algo_address = input("Enter the algod address: ")

    if sender["address"] is None:
        sender["address"] = input("Enter the sender address: ")

    if sender["mnemonic"] is None:
        sender["mnemonic"] = input("Enter the sender mnemonic: ")

    sender["private_key"] = mnemonic.to_private_key(sender["mnemonic"])

    asa_or_algo = input(
        "Do you want to transfer an ASA or ALGO? (asa or algo, default is algo): "
    ).lower()

    asa = False

    if asa_or_algo == "asa":
        asa = True
    else:
        asa = False

    print("\nTransfering ASA" if asa else "\nTransfering ALGO")
    print("\nInput transfer details below\n")

    if asa:
        asset_id = int(input("Enter the asset id: "))

    receiver = input("Enter the receiver address: ")
    amount = int(input("Enter the amount to transfer: "))
    note = input("Enter the note: ")

    if algo:
        amount = to_microalgos(amount)

    if asa:
        transfer_asset(sender, receiver, sender["private_key"], asset_id, amount, note)
        print("Asset transfer successful")
    else:
        transfer_algo(sender, receiver, sender["private_key"], amount, note)
        print("Algo transfer successful")
