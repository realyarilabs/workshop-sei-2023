## Setup

First, start by copying `.envrc_example` into `.envrc`.
Then fill `SENDER_ADDRESS` with the wallet address you just created.
Then fill `SENDER_MNEMONIC` with the wallet mnemonic for the wallet you created. You can obtain this mnemonic from the Web Developer Tools of your browser.

The `ALGOD_TOKEN` and the `ALGOD_ADDRESS` present on the `.envrc_example` are already correct for sandbox development.

**Note:** You must install `py-algorand-sdk` with `pip install py-algorand-sdk`.

## Generate ASAs or NFTs

To generate an ASA or a NFT you can simply run the `generate.py` script after completing the setup.

It will prompt you to provide the needed information and will create the asset on the network you are connected to.

```bash
python3 generate.py

# Example:
Do you want to create an ASA or an NFT? (ASA or NFT, ASA is the default):
Input token details (leave blank to use default values)

Enter the token name (defaults to Mega SEI Token):
Enter the token symbol (defaults to MST):
Enter the token decimals (defaults to 6):
Enter the token total supply (defaults to 21 million :wink:):
Enter the token url (defaults to ASA):
Enter the token reserve address (defaults to the asset creator):
Enter the token freeze address (defaults to the asset creator):
Enter the token clawback address (defaults to the asset creator):
Enter the token manager address (defaults to the asset creator):
```

## Transfering Algorand between accounts

To transfer assets between accounts you can simply run the `transfer.py` script after completing the setup.

It will prompt you to provide the needed information and will transfer either algorand or the provided ASA to the wallet you wish (from the wallet on the environment variables).

```
python3 transfer.py

# Example:
Do you want to transfer an ASA or ALGO? (asa or algo, default is algo):

Transfering ALGO

Input transfer details below

Enter the receiver address: FGQ2OEEVENWFVG74MAEJKT7COT6EUE3AAGG47ZTWK2MPID3IZ7ZIYTXRGY
Enter the amount to transfer: 10
Enter the note: hi!
Algo transfer successful
```

## Transfering an ASA between accounts

To transfer an ASA between accounts you can also run the `transfer.py`.
When it asks if you want to transfer an ASA or ALGO you should now put `asa`.

Warning: This might fail if the account you are transfering the ASA to has not yet opted into that ASA.

```
python3 transfer.py

# Fails because we haven't opted into the ASA yet
Do you want to transfer an ASA or ALGO? (asa or algo, default is algo): asa

Transfering ASA

Input transfer details below

Enter the asset id: 11
Enter the receiver address: FGQ2OEEVENWFVG74MAEJKT7COT6EUE3AAGG47ZTWK2MPID3IZ7ZIYTXRGY
Enter the amount to transfer: 10
Enter the note: hi!
Traceback (most recent call last):
...
algosdk.error.AlgodHTTPError: TransactionPool.Remember: transaction 2ER36NTTU4BX37MOBRH7ITVY6XU7U4OEGHZWR3CG5QPYPBDLC2VA: receiver error: must optin, asset 11 missing from FGQ2OEEVENWFVG74MAEJKT7COT6EUE3AAGG47ZTWK2MPID3IZ7ZIYTXRGY
```

To avoid the error above we can run the `opt_in.py` script and opt in to the ASA with the wallet we intend to receive it on.

```
python3 opt_in.py

# Successful opt in into the asset on the wallet we want to receive it
Enter the address of the account that will be opting in: FGQ2OEEVENWFVG74MAEJKT7COT6EUE3AAGG47ZTWK2MPID3IZ7ZIYTXRGY
Enter the mnemonic of the account that will be opting in: drink finish puzzle umbrella unique quote patrol settle feature convince grant impose victory deny rare below lens pride provide attack syrup peace author about truly
Enter the asset id: 11
Opted in to asset id: 11
```

If you try to do a transfer now it will work as expected.

```
python3 transfer.py

# Successful transfer of an ASA
Do you want to transfer an ASA or ALGO? (asa or algo, default is algo): asa

Transfering ASA

Input transfer details below

Enter the asset id: 11
Enter the receiver address: FGQ2OEEVENWFVG74MAEJKT7COT6EUE3AAGG47ZTWK2MPID3IZ7ZIYTXRGY
Enter the amount to transfer: 10
Enter the note: hi!
Asset transfer successful
```
