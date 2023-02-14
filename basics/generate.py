import os
import pdb

from algosdk.v2client import algod
from algosdk import mnemonic, account, constants, encoding, transaction


def create_asset(
    account,
    asset_name,
    asset_unit_name,
    asset_url,
    asset_manager,
    asset_reserve,
    asset_freeze,
    asset_clawback,
    amount,
    decimals,
):
    # Get the suggested parameters from the node
    params = algod_client.suggested_params()

    # Create the transaction
    txn = transaction.AssetConfigTxn(
        sender=account["address"],
        sp=params,
        total=amount,
        decimals=decimals,
        default_frozen=False,
        unit_name=asset_unit_name,
        asset_name=asset_name,
        url=asset_url,
        metadata_hash=None,
        manager=asset_manager,
        reserve=asset_reserve,
        freeze=asset_freeze,
        clawback=asset_clawback,
        strict_empty_address_check=False,
    )

    # Sign the transaction
    txn_signed = txn.sign(account["private_key"].encode())
    # Send the transaction
    txid = algod_client.send_transaction(txn_signed)
    # wait for the transaction to be confirmed
    transaction.wait_for_confirmation(algod_client, txid)

    # Get the new asset's information from the creator account
    account_info = algod_client.account_info(asset_manager)
    asset_id = account_info["created-assets"][-1]["index"]
    return asset_id


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

    # Ensure the user chooses ASA or NFT (default is ASA)
    asa_or_nft = (
        input(
            "Do you want to create an ASA or an NFT? (ASA or NFT, ASA is the default): "
        )
        or "ASA"
    ).lower()

    default_decimals = 6

    if asa_or_nft == "nft":
        asa_or_nft = "NFT"
        default_decimals = 0
    else:
        asa_or_nft = "ASA"

    print("Input token details (leave blank to use default values)\n")

    name = (
        input("Enter the token name (defaults to Mega SEI Token):") or "Mega SEI Token"
    )
    symbol = input("Enter the token symbol (defaults to MST):") or "MST"
    decimals = input("Enter the token decimals (defaults to {}):".format(default_decimals)) or default_decimals
    total = (
        input("Enter the token total supply (defaults to 21 million :wink:):")
        or 21000000
    )
    url = (
        input("Enter the token url (defaults to https://www.mydharma.network/):")
        or "https://www.mydharma.network/"
    )
    reserve = (
        input("Enter the token reserve address (defaults to the asset creator):")
        or sender["address"]
    )
    freeze = (
        input("Enter the token freeze address (defaults to the asset creator):")
        or sender["address"]
    )
    clawback = (
        input("Enter the token clawback address (defaults to the asset creator):")
        or sender["address"]
    )
    manager = (
        input("Enter the token manager address (defaults to the asset creator):")
        or sender["address"]
    )

    decimals = int(decimals)
    total = total * 10**decimals

    # If the user wants to create an NFT, we could add the @arc3 suffix to the name so explorers identify it as an NFT
    if asa_or_nft == "NFT":
        name = name + "@arc3"

    asset_id = create_asset(
        sender,
        name,
        symbol,
        url,
        sender["address"],
        reserve,
        freeze,
        clawback,
        total,
        decimals,
    )

    print("\nCreated {} with ID {}".format(asa_or_nft, asset_id))

    print(
        "You can find the asset at https://app.dappflow.org/explorer/asset/{}/transactions".format(
            asset_id
        )
    )
