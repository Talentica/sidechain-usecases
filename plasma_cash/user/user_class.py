import requests
import rlp
from ethereum import utils
from web3 import Web3
from web3.auto import w3

from plasma_cash.child_chain.block import Block
from plasma_cash.child_chain.transaction import Transaction


class User:

    def __init__(self, public_address, private_key, root_chain_provider=None, child_chain_provider=None, ):
        if root_chain_provider is None:
            self.web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
        else:
            self.web3 = Web3(Web3.HTTPProvider(root_chain_provider))
        if child_chain_provider is None:
            self.child_chain = "http://localhost:8546"
        else:
            self.child_chain = child_chain_provider
        if self.web3.isChecksumAddress(public_address):
            self.address = public_address
        else:
            self.address = self.web3.toChecksumAddress(public_address)
        self.key = utils.normalize_key(private_key)
        self.contract = None

    def make_contract_object(self, _contract_address, _contract_abi):
        if _contract_address is None or _contract_abi is None:
            return None
        _contract_address = self.web3.toChecksumAddress(_contract_address)
        self.contract = self.web3.eth.contract(address=_contract_address, abi=_contract_abi)

    def get_authority(self):
        try:
            return self.contract.functions.authority().call()
        except:
            return None

    def get_block(self, blk_num=None):
        try:
            if blk_num is None:
                response = requests.get(f'{self.child_chain}/block')
            else:
                response = requests.get(f'{self.child_chain}/block/{blk_num}')
            if response.status_code == 200:
                return rlp.decode(utils.decode_hex(response.content), Block)
        except :
            print("exception occur in get_block function")
            return None

    def get_transaction(self, blk_num, uid):
        try:
            block = self.get_block(blk_num)
            # print(block)
            return block.get_tx_by_uid(uid)
        except:
            return None

    def get_proof(self, blk_num, uid):
        try:
            blk_num = int(blk_num)
            uid = int(uid)
            payload = {'blknum': blk_num, 'uid': uid}
            response = requests.get(f'{self.child_chain}/proof', params=payload)
            if response.status_code == 200:
                return response.content
        except:
            print("exception occur in get_proof function")
            return None

    def make_transfer(self, prev_block, uid, amount, new_owner):
        try:
            new_owner = utils.normalize_address(new_owner)
            tx = Transaction(prev_block, uid, amount, new_owner)
            tx.sign(self.key)
            encoded_txn = rlp.encode(tx, Transaction).hex()
            payload = {'tx': encoded_txn}
            response = requests.post(f"{self.child_chain}/send_tx", data=payload)
            if response.status_code == 200:
                return response.status_code, response.content.hex()
            else:
                return response.status_code, None
        except:
            print("exception occur in make_transfer function")
            return None, None

    def deposit(self, amount, currency=None):
        # try:
        if currency is None:
            currency = '0x' + '00' * 20

        value = w3.toWei(amount, 'ether') if currency == '0x' + '00' * 20 else 0
        tx = self.contract.functions.deposit(currency, amount).buildTransaction(
            {'from': self.address, 'value': value}
        )
        tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
        signed = w3.eth.account.signTransaction(tx, self.key)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        return self.get_uid(tx_hash)
        # except:
        #     print("exception occur in deposit function to root_chain")
        #     return None

    def abort_deposit(self, uid):
        try:
            tx = self.contract.functions.abortDeposit(uid).buildTransaction(
                {'from': self.address}
            )
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in abort_deposit function to root_chain")
            return None

    def start_exit(self, pre_tx_blk_num, uid, tx_blk_num):
        try:
            prev_block = self.get_block(pre_tx_blk_num)
            block = self.get_block(tx_blk_num)

            prev_tx = prev_block.get_tx_by_uid(uid)
            prev_block.merklize_transaction_set()
            prev_tx_proof = prev_block.merkle.create_merkle_proof(uid)

            tx = block.get_tx_by_uid(uid)
            block.merklize_transaction_set()
            tx_proof = block.merkle.create_merkle_proof(uid)

            tx = self.contract.functions.startExit(
                rlp.encode(prev_tx),
                prev_tx_proof,
                pre_tx_blk_num,
                rlp.encode(tx),
                tx_proof,
                tx_blk_num
            ).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in start_exit function to root_chain")
            return None

    def start_deposit_exit(self, uid, tx_blk_num):
        try:
            block = self.get_block(tx_blk_num)

            tx = block.get_tx_by_uid(uid)
            block.merklize_transaction_set()
            tx_proof = block.merkle.create_merkle_proof(uid)

            tx = self.contract.functions.startDepositExit(
                rlp.encode(tx),
                tx_proof,
                tx_blk_num
            ).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in start_deposit_exit function to root_chain")
            return None

    def challenge_exit(self, uid, blk_num):
        try:
            block = self.get_block(blk_num)

            tx = block.get_tx_by_uid(uid)
            block.merklize_transaction_set()
            tx_proof = block.merkle.create_merkle_proof(uid)
            tx = self.contract.functions.challengeExit(
                uid,
                rlp.encode(tx),
                tx_proof,
                blk_num
            ).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in challenge_exit function to root_chain")
            return None

    def finalize_exit(self, uid):
        try:
            tx = self.contract.functions.finalizeExit(uid).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in finalize_exit function to root_chain")
            return None

    def is_challenge_existed(self, uid, blk_num):
        try:
            block = self.get_block(blk_num)
            tx = block.get_tx_by_uid(uid)
            tx = self.contract.functions.isChallengeExisted(
                uid,
                rlp.encode(tx)
            ).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in is_challenge_existed function to root_chain")
            return None

    def respond_challenge_exit(self, uid, challenge_blk_num, respond_blk_num):
        try:
            challenge_block = self.get_block(challenge_blk_num)
            challenge_tx = challenge_block.get_tx_by_uid(uid)

            respond_block = self.get_block(respond_blk_num)
            respond_tx = respond_block.get_tx_by_uid(uid)
            respond_block.merklize_transaction_set()
            respond_tx_proof = respond_block.merkle.create_merkle_proof(uid)

            tx = self.contract.functions.respondChallengeExit(
                uid,
                rlp.encode(challenge_tx),
                rlp.encode(respond_tx),
                respond_tx_proof,
                respond_blk_num
            ).buildTransaction({'from': self.address})
            tx['nonce'] = w3.eth.getTransactionCount(self.address, 'pending')
            signed = w3.eth.account.signTransaction(tx, self.key)
            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
            return tx_hash
        except:
            print("exception occur in respond_challenge_exit function to root_chain")
            return None

    def get_challenges(self, uid, challenge_number):
        try:
            return self.contract.functions.challenges(uid, challenge_number).call()
        except:
            return None

    def get_merkle_root(self, blk_num):
        try:
            return self.contract.functions.childChain(blk_num).call()
        except:
            return None

    def get_current_blk_num(self):
        try:
            return self.contract.functions.currentBlkNum().call()
        except:
            return None

    def get_deposit_count(self):
        try:
            return self.contract.functions.depositCount().call()
        except:
            return None

    def get_exits(self, uid):
        try:
            return self.contract.functions.exits(uid).call()
        except:
            return None

    def get_wallet(self, uid):
        try:
            return self.contract.functions.wallet(uid).call()
        except:
            return None

    def get_uid(self, tx_hash):
        receipt = w3.eth.getTransactionReceipt(tx_hash)
        myfilter = self.contract.eventFilter('Deposit', {'fromBlock': receipt.blockNumber, 'toBlock': receipt.blockNumber});
        eventlist = myfilter.get_all_entries()
        # print(type(eventlist))
        return eventlist[0].args.uid

    def get_block_num(self, uid, start_block=None):
        last_block = self.get_current_blk_num()
        if start_block is None:
            start_block = 1
        while start_block <= last_block:
            if self.get_transaction(last_block, uid) is not None:
                return last_block
            last_block = last_block - 1
        return -1
