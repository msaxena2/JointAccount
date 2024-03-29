import unittest
from ethereum import tester, utils


class Tests(unittest.TestCase):
    def get_compiled_contract(self):
        with open('serpent/joint_account.se', 'r') as code_file:
            serpent_code =  code_file.read()
        s = tester.state()
        test_contract = s.abi_contract(serpent_code)
        return s, test_contract

    def setUp(self):
        self.state, self.test_contract = self.get_compiled_contract()
        self.account_id = 1

    def test_create_account(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.assertEqual(50000, self.state.block.get_balance(self.test_contract.address))

    def test_create_and_join(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        retval = self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        self.assertEqual(retval, 1)

    def test_process_without_consent(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        k2_address = utils.privtoaddr(tester.k2)
        initial_balance = self.state.block.get_balance(k2_address)
        transaction_id = self.test_contract.propose_transaction(self.account_id, 5000, k2_address)
        self.test_contract.process_transaction(transaction_id)
        self.assertEqual(initial_balance, self.state.block.get_balance(k2_address))

    def test_process_with_consent(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        k2_address = utils.privtoaddr(tester.k2)
        initial_balance = self.state.block.get_balance(k2_address)
        transaction_value = 1000
        transaction_id = self.test_contract.propose_transaction(self.account_id, transaction_value, k2_address)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k1)
        self.test_contract.process_transaction(transaction_id)
        self.assertEqual(initial_balance + transaction_value, self.state.block.get_balance(k2_address))

    def test_process_withdraw(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k3, value=50000)
        k2_address = utils.privtoaddr(tester.k2)
        initial_balance = self.state.block.get_balance(k2_address)
        transaction_value = 1000
        transaction_id = self.test_contract.propose_transaction(self.account_id, transaction_value, k2_address, sender=tester.k0)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k1)
        self.test_contract.withdraw(self.account_id, sender=tester.k1)
        self.test_contract.process_transaction(transaction_id)
        self.assertEqual(initial_balance, self.state.block.get_balance(k2_address))


    def test_process_withdraw_consent(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k3, value=50000)
        k2_address = utils.privtoaddr(tester.k2)
        initial_balance = self.state.block.get_balance(k2_address)
        transaction_value = 10000
        transaction_id = self.test_contract.propose_transaction(self.account_id, transaction_value, k2_address, sender=tester.k0)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k1)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k3)
        self.test_contract.withdraw(self.account_id, sender=tester.k1)
        self.test_contract.process_transaction(transaction_id)
        self.assertEqual(initial_balance + transaction_value, self.state.block.get_balance(k2_address))


    def test_process_withdraw_consent_reward(self):
        self.test_contract.create_account(self.account_id, sender=tester.k0, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k1, value=50000)
        self.test_contract.join_account(self.account_id, sender=tester.k3, value=50000)
        k2_address = utils.privtoaddr(tester.k2)
        k4_address = utils.privtoaddr(tester.k4)
        initial_balance = self.state.block.get_balance(k4_address)
        transaction_value = 1000
        transaction_id = self.test_contract.propose_transaction(self.account_id, transaction_value, k2_address, sender=tester.k0)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k1)
        self.test_contract.consent_transaction(transaction_id, sender=tester.k3)
        self.test_contract.process_transaction(transaction_id, sender=tester.k4)
        self.assertGreater(50000 + initial_balance, self.state.block.get_balance(k4_address))

def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()