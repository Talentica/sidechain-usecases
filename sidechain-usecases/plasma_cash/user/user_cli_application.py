import configparser
import json
import sys
from generic.user_class import User


def block_explorer(_block):
    if _block is None:
        return
    print("---block explorer---")
    transaction_count = len(_block.transaction_set)
    print(transaction_count)
    for txn in _block.transaction_set:
        transaction_explorer(txn)
    print("--------------------")


def transaction_explorer(transaction):
    print('prev_block', transaction.prev_block),
    print('uid', transaction.uid),
    print('amount', transaction.amount),
    print('new_owner', transaction.new_owner.hex()),
    print('sig', transaction.sig)


def get_authority():
    print(user.get_authority())


def get_block():
    print("enter block number")
    try:
        blk_num = int(input())
        block_explorer(user.get_block(blk_num))
    except:
        block_explorer(user.get_block())


def get_transaction():
    try:
        print("provide following details->")
        print("block-number (integer value)")
        blk_num = int(input())
        print("uid (integer value)")
        uid = int(input())
        block = user.get_block(blk_num)
        transaction_explorer(block.get_tx_by_uid(uid))
    except:
        print("either transaction or arguments are invalid")


def transfer():
    try:
        print("provide following details->")
        print("previous-block-number (integer value)")
        prev_block = int(input())
        print("uid (integer value)")
        uid = int(input())
        print("amount")
        amount = int(input())
        print("new-owner address")
        new_owner = input()
        status_code, content = user.make_transfer(prev_block, uid, amount, new_owner)
        if status_code == 200:
            print(status_code, content)
        else:
            print(status_code)
    except:
        print("exception occur in transfer function")


def deposit():
    try:
        print("provide following details->")
        print("amount")
        amount = input()
        print("uid -> ", user.deposit(amount))
    except:
        print("exception occur in deposit function to root_chain")


def abort_deposit():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("tx_receipt ", user.abort_deposit(uid))
    except:
        print("exception occur in abort_deposit function to root_chain")


def start_exit():
    try:
        print("provide following details->")
        print("previous-transaction-block-number (integer value)")
        pre_tx_blk_num = int(input())
        print("uid (integer value)")
        uid = int(input())
        print("current-transaction-block-number (integer value)")
        tx_blk_num = int(input())
        print("tx_receipt ", user.start_exit(pre_tx_blk_num, uid, tx_blk_num))
    except:
        print("exception occur in start_exit function to root_chain")


def start_deposit_exit():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("deposit-transaction-block-number (integer value)")
        tx_blk_num = int(input())
        print("tx_receipt ", user.start_deposit_exit(uid, tx_blk_num))
    except:
        print("exception occur in start_deposit_exit function to root_chain")


def challenge_exit():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("deposit-transaction-block-number (integer value)")
        blk_num = int(input())
        print("tx_receipt ", user.challenge_exit(uid, blk_num))
    except:
        print("exception occur in challenge_exit function to root_chain")


def finalize_exit():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("tx_receipt ", user.finalize_exit(uid))
    except:
        print("exception occur in finalize_exit function to root_chain")
        return None


def is_challenge_existed():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("deposit-transaction-block-number (integer value)")
        blk_num = int(input())
        print("tx_receipt ", user.is_challenge_existed(uid, blk_num))
    except:
        print("exception occur in is_challenge_existed function to root_chain")


def respond_challenge_exit():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("challenge-transaction-block-number (integer value)")
        challenge_blk_num = int(input())

        print("respond-transaction-block-number (integer value)")
        respond_blk_num = int(input())
        print("tx_receipt ", user.respond_challenge_exit(uid, challenge_blk_num, respond_blk_num))
    except:
        print("exception occur in respond_challenge_exit function to root_chain")


def get_challenges():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("challenge number (integer value)")
        challenge_number = int(input())
        print(user.get_challenges(uid, challenge_number))
    except:
        print("provide correct inputs")


def get_current_blk_num():
    print(user.get_current_blk_num())


def get_deposit_count():
    print(user.get_deposit_count())


def get_exits():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print(user.get_exits(uid))
    except:
        print("provide correct inputs")


def get_wallet():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print(user.get_wallet(uid))
    except:
        print("provide correct inputs")


def get_uid():
    try:
        print("provide following details->")
        print("transaction-hash")
        tx_hash = input()
        print(user.get_uid(tx_hash))
    except:
        print("provide correct inputs")


def get_block_num():
    try:
        print("provide following details->")
        print("uid (integer value)")
        uid = int(input())
        print("start block (integer value)")
        start_block = input()
        if start_block == "":
            start_block = None
        else:
            start_block = int(start_block)
        print(user.get_block_num(uid, start_block))
    except:
        print("provide correct inputs")


if __name__ == '__main__':
    config = configparser.RawConfigParser()
    config.read('generic/user.properties')

    address = config.get('user', 'address')
    key = config.get('user', 'key')
    _root_chain_provider = config.get('user', 'root_chain_provider')
    _side_chain_provider = config.get('user', 'side_chain_provider')
    contract_address = config.get('contract', 'contract_address')
    contract_abi = config.get('contract', 'contract_abi')
    contract_abi = json.loads(contract_abi)
    user = User(public_address=address, private_key=key, root_chain_provider=_root_chain_provider,
                child_chain_provider=_side_chain_provider)

    user.make_contract_object(_contract_address=contract_address, _contract_abi=contract_abi)
    print("choose operation ")
    operation_choice = int(input())
    while operation_choice != -1:
        print("operation_choice ", operation_choice)
        switcher = {
            0: get_authority,
            1: get_block,
            2: get_transaction,
            3: transfer,
            4: deposit,
            5: abort_deposit,
            6: start_exit,
            7: start_deposit_exit,
            8: challenge_exit,
            9: finalize_exit,
            10: is_challenge_existed,
            12: respond_challenge_exit,
            13: get_challenges,
            14: get_current_blk_num,
            15: get_deposit_count,
            16: get_exits,
            17: get_wallet,
            18: get_uid,
            19: get_block_num,
        }
        case = switcher.get(operation_choice, "Invalid operation")
        if type(case) == str:
            print(case)
            sys.exit()
        case()
        print("choose operation ")
        operation_choice = int(input())
