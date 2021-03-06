#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account
from algosdk.future.transaction import PaymentTxn
import json

#Connect to Algorand node maintained by PureStake
#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'

headers = {
   "X-API-Key": algod_token,
}
acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

#private_key, public_address = account.generate_account()
#print("Base64 Private Key: {}\nPublic Algorand Address: {}\n".format(private_key, public_address))
#mnemonic_secret = mnemonic.from_private_key(private_key)
#print("mnemonic_secret = \"{}\"".format(mnemonic_secret))
#mnemonic_secret = "daughter coin decorate junior shift much soft pottery change chase they family culture program salute stool angry chapter cake congress sugar castle inject above stable"
mnemonic1 = "daughter coin decorate junior shift much soft pottery change chase they family culture program salute stool angry chapter cake congress sugar castle inject above stable"
sk = mnemonic.to_private_key(mnemonic1)
pk = mnemonic.to_public_key(mnemonic1)
#print("My address: {}".format(pk))
account_info = acl.account_info(pk)
#print(json.dumps(account_info, indent=4))
#print("Account balance: {} microAlgos".format(account_info.get('amount')))


def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    sender_pk = pk
    params.fee = tx_amount
    receiver = receiver_pk
    unsigned_txn = PaymentTxn(sender_pk, params, receiver_pk, tx_amount)
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(mnemonic1))
    txid = acl.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))
    
    return sender_pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

