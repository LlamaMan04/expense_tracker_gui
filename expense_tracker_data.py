from enum import Enum

class Profile:
    """ Top-level class to store information about different accounts
    together. 
    """

    def __init__(self, name, accounts=None):
        """ Initializer method.
        """
        
        self.name = name

        # If we have been given an accounts list, assign it. Otherwise, 
        # create it as an empty list. 
        if accounts != None:
            self.accounts = accounts

            # Make sure each account correctly points to this object
            # as its parent profile. 
            for account in self.accounts:
                account.profile = self
        else:
            self.accounts = []

    def get_account_names(self):
        """Returns a list of the names of each account in self.accounts.
        """

        names = []
        for account in self.accounts:
            names.append(account.name)
        return names
    
    def get_account_from_name(self, account_name):
        """ Returns the account object with the given name, or None if
        the account does not exist. 
        """

        for account in self.accounts:
            if account.name == account_name:
                return account
            
        return None
    
    def add_account(self, account):
        """ Adds the provided account to self.accounts and updates the
        account's profile reference to point to this object. 
        """

        self.accounts.append(account)
        account.profile = self

    def remove_account(self, account):
        """ Removes the given account from self.accounts.
        """

        self.accounts.remove(account)

class Account:
    """ Class to store information about each account in the profile.
    """

    def __init__(self, name, balance=0, transactions=None):
        """ Initializer method
        """

        self.name = name
        self.balance = balance

        # If we have been given a transactions list, assign it. 
        # Otherwise, create it as an empty list. 
        if transactions != None:
            self.transactions = transactions
            # Make sure the account pointer in each transaction points
            # to this account. 
            for trans in self.transactions:
                trans.account = self
        else:
            self.transactions = []

    def add_trans(self, trans):
        """ Adds a new transaction to self.transactions, updates the 
        account balance based on the amount of the new transaction, and 
        updates the transaction account pointer to point to this 
        account. 
        """

        # Add transaction to list
        self.transactions.append(trans)

        # Update account balance.
        if trans.type == TransType.EXPENSE:
            self.balance -= trans.amount
        else:
            self.balance += trans.amount

        # Update transaction account pointer.
        trans.account = self

    def trans_amount_change(self, old_amount, new_amount, type):
        """ Updates the account balance after a change to a transaction
        amount. 
        """

        if type == TransType.EXPENSE:
            self.balance += old_amount
            self.balance -= new_amount
        else:
            self.balance -= old_amount
            self.balance += new_amount

    def remove_trans(self, trans):
        """ Removes the given transaction from self.transaction and 
        removes its effect on the account balance. 
        """

        # Update balance.
        if trans.type == TransType.EXPENSE:
            self.balance += trans.amount
        else:
            self.balance -= trans.amount

        # Remove from transactions list.
        self.transactions.remove(trans)

class Transaction:
    """ Class to store information about each transaction entered in an 
    account. 
    """

    def __init__(self, amount, description, date, type):
        """ Initializer method. Assigns the given values.
        """

        self.amount = amount
        self.description = description
        self.date = date
        self.type = type

    def update_amount(self, new_amount):
        """ Updates the amount in the transaction and handles updating 
        the balance of the parent account as well. 
        """

        self.account.trans_amount_change(self.amount, new_amount, self.type)
        self.amount = new_amount

class TransType(Enum):
    """ Enum class used to store the type of a Transaction
    """

    EXPENSE = 0
    INCOME = 1