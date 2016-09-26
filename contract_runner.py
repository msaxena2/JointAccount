import serpent
from ethereum import tester, abi, utils


def create_contract():
    with open('serpent/joint_account.se', 'r') as code_file:
        serpent_code =  code_file.read()
    s = tester.state()
    return s.abi_contract(serpent_code)


if __name__ == '__main__':
    test_contract = create_contract()
    test_contract.create_account("blah", sender=tester.k0, value=10)
    print test_contract.get_joining_amount("blah")

