import serpent
from ethereum import tester, abi, utils


if __name__ == '__main__':
    with open('serpent/joint_account.se', 'r') as code_file:
        serpent_code =  code_file.read()
    s = tester.state()
    test_contract = s.abi_contract(serpent_code)
    test_contract.create_account(1, sender=tester.k0, value=10)
    test_contract.join_account(1, sender=tester.k1, value=11)
    transaction = test_contract.propose_transaction(1, 10, utils.privtoaddr(tester.k2), sender=tester.k0)
    #test_contract.consent_transaction(transaction, sender=tester.k1)
    #test_contract.withdraw(1, sender=tester.k1)
    test_contract.process_transaction(transaction)
    tester_key = utils.privtoaddr(tester.k2)
    print s.block.get_balance(tester_key)

