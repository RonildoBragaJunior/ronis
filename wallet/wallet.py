from random import randint
import uuid
import time


class Transaction:

    def __init__(self, prev_address=None, address=None, amount=0, fee=0, time=time.time()):
        self.prev_address = prev_address
        self.address = address
        self.amount = amount
        self.fee = fee
        self.time = time


class Wallet:
    utxns = []
    wallet_address = str(uuid.uuid4())

    def move_transaction(self, input_transactions, new_address, amount):
        prev_address = []
        total_amount = amount

        for input_transaction in input_transactions:
            prev_address.append(input_transaction)

            if input_transaction.amount > amount:
                new_transaction = Transaction(
                    prev_address=prev_address,
                    address=new_address,
                    amount=total_amount
                )
                if input_transaction.amount - amount > 0:
                    rest_transaction = Transaction(
                        prev_address=[input_transaction],
                        address=self.wallet_address,
                        amount=input_transaction.amount - amount
                    )
            else:
                amount -= input_transaction.amount

        return new_transaction, rest_transaction
