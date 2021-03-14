import time

limits = {"balance": -1, "topUp": -1, "withdrawal": -1}
accounts = {}
txnlog = []

def topUp(account, amount):
    if account not in accounts:
        raise Exception("account not found")

    limit = limits['topUp']

    if limit != -1:
        if amount > limit:
            raise Exception('not allowed')

    accounts[account]['balance'] = accounts[account]['balance'] + amount
    txnlog.append({time.time(): ("topUp<account: %d, amount: %d>", (int(account), int(amount),))})

def withdraw(account, amount):
    if account not in accounts:
        raise Exception('account not found')

    limit = limits['withdrawal']
    if limit == -1:
        limit = accounts[account]['balance']
    accounts[account]['balance'] = accounts[account]['balance'] - amount

    txnlog.append({time.time(): ("withdrawal<account: %d, amount: %d>", (int(account), int(amount),))})

def transfer(from_account, to_account, amount, comment=''):
    withdraw(from_account, amount)
    topUp(to_account, amount)
    if comment:
        txnlog[-2]['comment'] = comment 
        txnlog[-1]['comment'] = comment 

