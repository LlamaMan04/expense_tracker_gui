import pytest, os, pickle
from expense_tracker_gui import InputGUIParent, DateInput
from expense_tracker_main import Controller
from expense_tracker_data import *
from datetime import datetime, date

def test_validate_entry_name():
    """ Test function for the InputGUIParent.validate_entry_name
    method. Verifies that this method accurately decides whether
    the given input is valid. 
    """

    # Instantiate the object to allow calling the method. 
    obj = InputGUIParent()

    # Verify return is correct type. 
    test = obj.validate_entry_name("abc")
    assert isinstance(test, bool), "Method must return a boolean value."
    test = obj.validate_entry_name("+-*")
    assert isinstance(test, bool), "Method must return a boolean value."

    # Verify return is correct value. 
    assert obj.validate_entry_name("") == True
    assert obj.validate_entry_name("Abcdef") == True
    assert obj.validate_entry_name("Abc123") == True
    assert obj.validate_entry_name("12345") == True
    assert obj.validate_entry_name("ab,cd") == False
    assert obj.validate_entry_name("ab+*cd") == False
    assert obj.validate_entry_name("+*") == False

def test_validate_entry_money_value():
    """ Test function for the InputGUIParent.validate_entry_money_value
    method. Verifies that this method accurately decides whether
    the given input is valid. 
    """

    # Instantiate the object to allow calling the method. 
    obj = InputGUIParent()

    # Verify return is correct type. 
    test = obj.validate_entry_money_value("20.1")
    assert isinstance(test, bool), "Method must return a boolean value."
    test = obj.validate_entry_money_value("+-*")
    assert isinstance(test, bool), "Method must return a boolean value."

    # Verify return is correct value. 
    assert obj.validate_entry_money_value("") == True
    assert obj.validate_entry_money_value("0") == True
    assert obj.validate_entry_money_value("-1") == True
    assert obj.validate_entry_money_value("123456") == True
    assert obj.validate_entry_money_value("1.1") == True
    assert obj.validate_entry_money_value("1.12") == True
    assert obj.validate_entry_money_value("1.123") == False
    assert obj.validate_entry_money_value("-1.1") == True
    assert obj.validate_entry_money_value("-1.123") == False
    assert obj.validate_entry_money_value("1.1.23") == False
    assert obj.validate_entry_money_value("1..123") == False
    assert obj.validate_entry_money_value("--123") == False
    assert obj.validate_entry_money_value("-1-23") == False

def test_is_valid_date():
    """ Test function for the DateInput.is_valid_date static method. 
    Verifies that the method accurately determines if a given string
    is a valid date. 
    """

    # Verify return is correct type. 
    test = DateInput.is_valid_date("01/02/2004")
    assert isinstance(test, bool), "Method must return a boolean value."
    test = DateInput.is_valid_date("abcdefghi")
    assert isinstance(test, bool), "Method must return a boolean value."

    # Verify return is correct value. 
    assert DateInput.is_valid_date("") == False
    assert DateInput.is_valid_date("abcdefghij") == False
    assert DateInput.is_valid_date("0123456789") == False
    assert DateInput.is_valid_date("00/00/0000") == False
    assert DateInput.is_valid_date("99/99/9999") == False
    assert DateInput.is_valid_date("01/32/2004") == False
    assert DateInput.is_valid_date("13/30/2004") == False
    assert DateInput.is_valid_date("02/29/2003") == False
    assert DateInput.is_valid_date("02/29/2004") == True
    assert DateInput.is_valid_date("01/01/2004") == True
    assert DateInput.is_valid_date("06/24/1995") == True

def test_profile_constructor():
    """ Test function for the constructor for the Profile class. 
    Verifies that the attributes are correctly assigned. 
    """

    # Verify that a profile without accounts creates correctly. 
    test_profile_1 = Profile("Test 1")
    assert test_profile_1.name == "Test 1"
    assert test_profile_1.accounts == []

    # Verify that a profile with accounts creates correctly. 
    test_accounts = [Account("Test Account", 200), 
                     Account("Test Account 2", 300)]
    test_profile_2 = Profile("Test 2", test_accounts)
    assert test_profile_2.name == "Test 2"
    assert test_profile_2.accounts == test_accounts

def test_get_account_names():
    """ Test function for the Profile.get_account_names method. Verifies
    that it returns an accurate list of strings containing the name of
    each account it contains. 
    """

    # Initialize the object, confirm the list initally returns empty. 
    test_profile = Profile("Test Profile")
    assert test_profile.get_account_names() == []

    # Add an account, confirm the list reflects the change. 
    test_profile.add_account(Account("Test Account 1", balance=200))
    assert test_profile.get_account_names() == ["Test Account 1"]

    # Add an account, confirm the list reflects the change. 
    test_profile.add_account(Account("Test Account 2", balance=400))
    assert test_profile.get_account_names() == ["Test Account 1", 
                                                "Test Account 2"]

def test_get_account_from_name():
    """ Test function for the Profile.get_account_from_name method. 
    Verifies that it returns the correct account when provided an 
    account name, or None if it doesn't exist. 
    """

    # Initialize the object, confirm the method returns None.  
    test_profile = Profile("Test Profile")
    assert test_profile.get_account_from_name("Test") == None

    # Add an account, confirm the method can find it.
    test_account_1 = Account("Test Account 1", balance=200)
    test_profile.add_account(test_account_1)
    assert test_profile.get_account_from_name("Test Account 1") == \
                                            test_account_1

    # Add another account, confirm the method can find it as well.  
    test_account_2 = Account("Test Account 2", balance=400)
    test_profile.add_account(test_account_2)
    assert test_profile.get_account_from_name("Test Account 2") == \
                                            test_account_2

    # Confirm that the method returns None if given an invalid name.
    assert test_profile.get_account_from_name("Fake name") == None

def test_add_account():
    """ Test function for the Profile.add_account method. Verifies that 
    it properly adds the account to the object's list and correctly
    assigns the account.profile pointer. 
    """

    # Initialize the object.
    profile = Profile("Test Profile")

    # Add an account, confirm the list reflects it and the account's 
    # profile pointer was updated.
    account_1 = Account("Test 1", 200)
    profile.add_account(account_1)
    assert profile.accounts == [account_1]
    assert account_1.profile == profile

    # Add another account, confirm the list reflects it and the 
    # account's profile pointer was updated.
    account_2 = Account("Test 2", 400)
    profile.add_account(account_2)
    assert profile.accounts == [account_1, account_2]
    assert account_2.profile == profile

def test_remove_account():
    """ Test function for the Profile.remove_account method. Verifies that 
    it properly removes the account from the object's list.
    """

    # Initialize the object and add a few test accounts.
    account_1 = Account("Test 1", 200)
    account_2 = Account("Test 2", 400)
    profile = Profile("Test Profile", [account_1, account_2])

    # Remove an account, confirm the list reflects it.
    profile.remove_account(account_1)
    assert profile.accounts == [account_2]

    # Remove another account, confirm the list reflects it and the 
    # account's profile pointer was updated.
    profile.remove_account(account_2)
    assert profile.accounts == []

def test_account_constructor():
    """ Test function for the constructor for the Account class. 
    Verifies that the attributes are correctly assigned. 
    """

    # Verify that an account without transactions creates correctly. 
    test_account_1 = Account("Test 1", 200)
    assert test_account_1.name == "Test 1"
    assert test_account_1.balance == 200
    assert test_account_1.transactions == []

    # Verify that an account with transactions creates correctly. 
    test_trans = [
        Transaction(35.6, "Test Trans 1", date.today(), TransType.EXPENSE), 
        Transaction(38.4, "Test Trans 2", date.today(), TransType.INCOME)]
    test_account_2 = Account("Test 2", 300.25, test_trans)
    assert test_account_2.name == "Test 2"
    assert test_account_2.balance == 300.25
    assert test_account_2.transactions == test_trans

def test_add_trans():
    """ Test function for the Account.add_trans method. Verifies that 
    it properly adds the transaction to the object's list, correctly 
    updates the account balance, and correctly assigns the 
    transaction.account pointer. 
    """

    # Initialize the object.
    account = Account("Test Account", 400)

    # Add a transaction, confirm the list reflects it and the account 
    # balance and transaction account pointer updated correctly.
    trans_1 = Transaction(100, "Test 1", date.today(), TransType.EXPENSE)
    account.add_trans(trans_1)
    assert account.transactions == [trans_1]
    assert account.balance == 300
    assert trans_1.account == account

    # Add another transaction, confirm the list reflects it and the 
    # account balance and transaction account pointer updated correctly.
    trans_2 = Transaction(100, "Test 2", date.today(), TransType.INCOME)
    account.add_trans(trans_2)
    assert account.transactions == [trans_1, trans_2]
    assert account.balance == 400
    assert trans_2.account == account

def test_trans_amount_change():
    """ Test function for the Account.trans_amount_change. Verifies that
    the function accurately adjusts the account balance given a change
    in transaction amounts.
    """

    # Create an object to test with. 
    account = Account("Test Account", 400)

    # Update the balance and verify
    account.trans_amount_change(100, 150, TransType.EXPENSE)
    assert account.balance == 350

    # Update the balance and verify
    account.trans_amount_change(100, 150, TransType.INCOME)
    assert account.balance == 400

    # Update the balance and verify
    account.trans_amount_change(100, 199.50, TransType.EXPENSE)
    assert account.balance == 300.50

def test_remove_trans():
    """ Test function for the Account.remove_trans method. Verifies that 
    it properly removes the transaction from the object's list and 
    removes the transaction's effect on the account balance.
    """

    # Initialize the object and add a few test transactions.
    trans_1 = Transaction(100, "Test 1", date.today(), TransType.EXPENSE)
    trans_2 = Transaction(100, "Test 2", date.today(), TransType.INCOME)
    account = Account("Test Account", 400, [trans_1, trans_2])

    # Remove a transaction, confirm the list reflects it and the balance 
    # was updated accordingly. 
    account.remove_trans(trans_1)
    assert account.balance == 500
    assert account.transactions == [trans_2]

    # Remove another transaction, confirm the list reflects it and the 
    # balance was updated accordingly. 
    account.remove_trans(trans_2)
    assert account.balance == 400
    assert account.transactions == []

def test_transaction_constructor():
    """ Test function for the Transaction constructor, verifies that
    values are properly assigned. 
    """

    trans_1 = Transaction(200.46, "Test desc", date.today(), TransType.EXPENSE)
    assert trans_1.amount == 200.46
    assert trans_1.description == "Test desc"
    assert trans_1.date == date.today()
    assert trans_1.type == TransType.EXPENSE

    date_2 = datetime.strptime("02/29/2004", "%m/%d/%Y").date()
    trans_2 = Transaction(-100, "Test desc 2", date_2, TransType.INCOME)
    assert trans_2.amount == -100
    assert trans_2.description == "Test desc 2"
    assert trans_2.date == date_2
    assert trans_2.type == TransType.INCOME

def test_update_amount():
    """ Test function for the Transaction.update_amount method. Verifies
    that it correctly updates the transaction amount and also updates
    the parent account's balance. 
    """

    # Initialize objects to test on. 
    trans_1 = Transaction(200, "Test 1", date.today(), TransType.EXPENSE)
    trans_2 = Transaction(100, "Test 2", date.today(), TransType.INCOME)
    account = Account("Test Account", 400, [trans_1, trans_2])

    # Test updating an Expense type transaction.
    trans_1.update_amount(250)
    assert trans_1.amount == 250
    assert trans_1.account.balance == 350

    # Test updating an Income type transaction.
    trans_2.update_amount(150)
    assert trans_2.amount == 150
    assert trans_2.account.balance == 400

def test_load_from():
    """ Test function for the Controller.load_from method. Verifies that
    it properly loads a Profile object from a file containing one. 
    """

    # Get a controller object without calling its __init__ method. 
    controller = Controller.__new__(Controller)

    # Save a Profile object to a test file.
    profile_1 = Profile("Test Profile")
    with open("TestFile.etpk", 'wb') as file:
        pickle.dump(profile_1, file)

    # Load it and verify.
    load_profile = controller.load_from("TestFile.etpk")
    assert load_profile.name == profile_1.name
    assert load_profile.accounts == profile_1.accounts

    # Save another Profile object to the test file.
    profile_2 = Profile("Test Profile", [
        Account("Test Account 1", 100),
        Account("Test Account 2", 300)
    ])
    with open("TestFile.etpk", 'wb') as file:
        pickle.dump(profile_2, file)

    # Load it and verify.
    load_profile = controller.load_from("TestFile.etpk")
    assert load_profile.name == profile_2.name
    assert load_profile.accounts[0].name == profile_2.accounts[0].name
    assert load_profile.accounts[0].balance == profile_2.accounts[0].balance
    assert load_profile.accounts[1].name == profile_2.accounts[1].name
    assert load_profile.accounts[1].balance == profile_2.accounts[1].balance

    # Remove the test file.
    path = os.path.abspath("TestFile.etpk")
    os.remove(path)

def test_save_to():
    """ Test function for the Controller.save_to method. Verifies that
    it properly saves a Profile object to a file. 
    """

    # Get a controller object without calling its __init__ method. 
    controller = Controller.__new__(Controller)

    # Save a Profile object to a test file.
    profile_1 = Profile("Test Profile")
    controller.active_profile = profile_1
    controller.save_to("TestFile.etpk")

    # Load it and verify.
    with open("TestFile.etpk", 'rb') as file:
        load_prof = pickle.load(file)
    assert load_prof.name == profile_1.name
    assert load_prof.accounts == profile_1.accounts
    assert controller.active_file_path == "TestFile.etpk"

    # Save a Profile object with accounts to a test file.
    profile_2 = Profile("Test Profile", [
        Account("Test Account 1", 100),
        Account("Test Account 2", 300)
    ])
    controller.active_profile = profile_2
    controller.save_to("TestFile.etpk")

    # Load it and verify.
    with open("TestFile.etpk", 'rb') as file:
        load_prof = pickle.load(file)
    assert load_prof.name == profile_2.name
    assert load_prof.accounts[0].name == profile_2.accounts[0].name
    assert load_prof.accounts[0].balance == profile_2.accounts[0].balance
    assert load_prof.accounts[1].name == profile_2.accounts[1].name
    assert load_prof.accounts[1].balance == profile_2.accounts[1].balance
    assert controller.active_file_path == "TestFile.etpk"

    # Remove the test file.
    path = os.path.abspath("TestFile.etpk")
    os.remove(path)

# Call the main pytest function to execute the tests. 
pytest.main(["-v", "--tb=line", "-rN", __file__])