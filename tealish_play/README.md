# tealish_play

The goal of these scripts is test writing some smart contracts in tealish, deploy and iteract with them from python

1 - Install tealish (https://github.com/tinymanorg/tealish) 

```shell 
pip install tealish
```

2 - Compile your tealish source code
```
tealish compile sample_contract.tl
```
In this case 
```
tealish compile prize_counter.tl 
```

It will compile the tealish code to build/prize_counter.teal


The script deploy_and_run_from_tealish.py 
ilustrates how to compile from pyteal into teal and then into bytecode
or just how to use the compiled teal file from build.

```python

# Compile our contract
# approval_teal = compileTeal(approval_program(), Mode.Application, version=5)
clearstate_teal = compileTeal(approval_program(), Mode.Application, version=5)

# compile our teal to bytecode (its returned in bas64)
approval_b64 = algod_client.compile(load_teal_approval_program())["result"]
clearstate_b64 = algod_client.compile(clearstate_teal)["result"]

# decode the base64
approval_bytes = encoding.base64.b64decode(approval_b64)
clearstate_bytes = encoding.base64.b64decode(clearstate_b64)

```

The clearstate_teal is compiled from a very simple pyteal file
and the approval_b64 is directly loaded from the compiled tealish file

The script then proceeds to deploy the contract, fund it and interact with it 
until we reach the 10 call so the funds are returned to the sender 
and the contract can't be called again.

This can be verified on the algokit sandbox.

Before you run the script don't forget to setup and Fund the sender account on the sandbox.
