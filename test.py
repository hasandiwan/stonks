import app

import pytest

@pytest.fixture
def accounts():
    app.accounts = {1: {"balance": 100}, 2: {"balance": 150}, 3: {"balance": 1}}
    app.limits = {'balance': -1, 'topUp': -1, 'withdrawal': -1}

    yield

    app.accounts = {1: {"balance": 100}, 2: {"balance": 150}, 3: {"balance": 1}}
    app.limits = {'balance': -1, 'topUp': -1, 'withdrawal': -1}


# Integration/Acceptance tests
def testCanTopUp(accounts):
    old_amount = app.accounts[1].get('balance')
    app.topUp(1, 100)
    assert app.accounts[1].get('balance') - old_amount == 100

def testCanWithdraw(accounts):
    old_amount = app.accounts[1].get('balance')
    app.withdraw(1, 100)
    assert old_amount - app.accounts.get(1).get('balance') == 100

def testCanTransferFundsWithComments(accounts):
    old_account1 = app.accounts.get(2).get('balance')
    old_account2 = app.accounts.get(3).get('balance')
    app.transfer(2, 3, 100, comment='beer')
    assert app.accounts.get(2).get('balance') == 50
    assert app.accounts.get(3).get('balance') == 101

def testRequireCommentForTransfer(accounts):
    old_account1 = app.accounts.get(2).get('balance')
    old_account2 = app.accounts.get(3).get('balance')

    with pytest.raises(Exception):
        app.transfer('2', '3', 100)

def testCanSetLimits(accounts):
    app.limits['balance'] = 50
    assert app.limits['balance'] == 50

    app.limits['topUp'] = 1000
    assert app.limits['topUp'] == 1000

    app.limits['withdrawal'] = 800
    assert app.limits['withdrawal'] == 800

def testTopUpLimitIsEnforced(accounts):
    app.limits['topUp'] = 1000
    with pytest.raises(Exception):
        app.topUp(1, 1200)


def testWritesTxnLog(accounts):
    old_len = len(app.txnlog)
    app.transfer(1,2,1)
    assert len(app.txnlog) > old_len
