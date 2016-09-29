## 1 The Joint Account Smart Contract 1.1 Purpose of the contract
The smart contract aims to establish a system of accounts, which users of the contract can use to hold funds in, and collectively conduct transactions from. In order to use the account, a user can propose transactions to other users of the account, who then vote to decide whether the transaction should be upheld or not. Users are allowed to leave the account, but they are penalized for doing so.
### 1.2 Motivation
The contract is meant to provide decentralized banking services. In a way, it’s a DAO.
### 1.3 Use Case - Honest Entities
#### 1.3.1 Creating and Joining Accounts
Let’s consider an example of how the contract is supposed to behave when used by entities that don’t have intentions of exploiting the system. A person can open a new account by calling the create account method. When opening a new account, the user must supply an id, which the contract uses to identify the account, and some ether, which will be held in the account.
New users can join the account by calling the join account method, and supplying the id of the contract they wish to join. Users must also supply the method with a certain joining amount, which must be equal to, the total amount held in the account divided by the number of users in the account (before the new user joins). An extra ether supplied by the user is refunded. In order to find out the joining amount, a user can call the get joining amount method, with the id of the account he wishes to join.
#### 1.3.2 Conducting Transactions
A user can propose a transaction by calling the propose transaction method. In order to propose a transaction, the user must provide the id for an account, the spend amount, and

a public address for the outgoing transaction. A user can only propose a transaction if he’s a member of the account he wishes to use, and is automatically considered to have given consent to any transaction he proposes. The transaction id is returned if the call is successful. Other users can give consent to the transaction by calling the consent transaction method with the transaction id. Transactions are processed when a user calls the process transaction method.
#### 1.3.3 Withdrawing From an Account
A user can withdraw from an account, by calling the withdraw function, and supplying the id of the account he wishes to withdraw from.
### 1.4 Use Case - Dishonest Entities
We now discuss ways in which a user can try to exploit a contract, and mechanisms in place to prevent such exploits.
#### 1.4.1 Consenting a Transaction and Leaving
A user can try to provide his consent to a transaction, and then leave before the transaction is processed with his share of the money in the account. In such a case, other users would have to bear the cost of the transaction, and the malicious user might benefit from the transaction that he consented to. The contract ensures that while processing transactions, votes of users who left after giving consent are not counted in deciding consent. Also, users are penalized for leaving, and have to forfeit 50% of their share as penalty.
#### 1.4.2 Reentrancy - The DAO bug
The contract ensures that a user cannot the withdraw function recursively using a simple check. When the user calls the withdraw function for the first time, his address is placed in map. Before any calls are processed, the contract checks the map to ensure that the user’s address is not already in the map. If the user’s address is found in the map, the contract assumes a reentry attack, and denies the withdraw request.
### 1.5 Design Choices
An interesting design choice had to be made while dealing with the case of an account that users have withdrawn from. A user withdrawal leaves an account in an exceptional state. Consider a user A, who withdrew from an account x. After the withdrawal, every transaction dealing with x needs to take into account the fact that total number of members in the account has changed. There may also be transactions that have the required consensus to go through after x′s withdrawal. The process of going through and adjusting every proposed transaction in A whenever a user quits is expensive. Thus, the contract does not adjust numbers for every transaction, and allows transactions to remain in an inconsistent state. Instead, it promotes users to choose the transactions they’d like to be processed, and adjusts


the numbers only for the user-chosen transactions. A user can call the process transaction on any transaction, and the consensus numbers for the transaction are calculated (taking into account users who quit) at that moment. If there is consensus after adjusting the numbers, the transaction is approved. In order to incentivize users into regularly calling the process transaction method, a small reward is sent to the caller if the transaction is successful. This cost is borne by all members of the account, and can be though of as a minor transaction fee.
1.6 Testing Contract Code
The contract runner.py file has unit tests that test the contract for edge cases, such as making sure that vote of a user is not counted after he withdraws from the contract, and transactions that have consensus after user withdrawals are processed correctly. The tests can be run by simple calling ′python contract runner.py′.