import tkinter as tk
from tkinter import ttk, messagebox
from expense_tracker_data import *
from datetime import datetime, timedelta, date

class ExpenseTrackerGUI:
    """ Class that contains GUI setup information and helper functions
    for the main GUI window. 
    """

    def __init__(self, controller, profile=None):

        # Cache a reference to the controller and give it a reference
        # to this object since the value never returns due to the
        # tkinter infinite mainloop. 
        self.controller = controller
        self.controller.main_gui = self

        # Initialize the root GUI window. 
        self.root = tk.Tk()
        self.root.geometry("1000x800")
        self.root.title("Expense Tracker")
        self.root.protocol('WM_DELETE_WINDOW', controller.exit_confirm)

        # Setup File Menu options.
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Profile", command=controller.new_profile)
        self.filemenu.add_command(label="Open Profile", command=controller.load)
        self.filemenu.add_command(label="Save", command=controller.save)
        self.filemenu.add_command(label="Save As", command=controller.save_as_new_profile)
        self.filemenu.add_command(label="Save and Exit", command=controller.save_and_exit)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.root.config(menu=self.menubar)

        # Setup title.
        self.heading = tk.Label(self.root, text="Expense Report", 
                                font=("Arial", 20))
        self.heading.pack(padx=10, pady=10)

        # Frame for layout. 
        self.layout = tk.Frame(self.root)
        self.layout.pack(fill='x', padx=0, pady=0, anchor='n')

        # Profile name.
        self.profile_title = tk.Label(self.layout, text="Profile:", font=('Arial', 12))
        self.profile_title.pack(side='left', padx=10, pady=10)

        # Add Account button
        self.add_account_button = tk.Button(self.layout, text="Add Account", font=('Arial', 14))
        self.add_account_button.pack(side='right', padx=10, pady=10)

        # Account selector dropdown. 
        self.account_selector = ttk.Combobox(self.layout, state="readonly", font=('Arial', 14))
        self.root.option_add("*TCombobox*Listbox*Font", ('Arial', 14)) 
        self.account_selector.pack(side='top', padx=10, pady=10)

        # Transaction display region.
        self.trans_region = VerticalScrolledFrame(self.root)
        self.trans_region.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Save and Exit button.
        self.exit_button = tk.Button(self.root, text="Save and Exit", font=('Arial', 14), command=self.controller.save_and_exit)
        self.exit_button.pack(side='right', anchor='s', padx=15, pady=15)

        if profile != None:
            # If we have been passed a profile object, set up the GUI
            # with that info.
            self.setup_profile_in_gui(profile)

        # Build the GUI.
        self.root.mainloop()

    def setup_profile_in_gui(self, profile):
        """ Updates the values of display objects in the main GUI 
        window to match the information in the active profile. 
        """

        # Configure profile name.
        self.profile_title.config(text=f"Profile: {profile.name}")

        # Configure add account button command.
        self.add_account_button.config(command=lambda: self.add_account(profile))

        # Configure account selector dropdown options and update 
        # command.
        self.account_selector.config(values=profile.get_account_names())
        self.account_selector.set("")
        self.account_selector.bind("<<ComboboxSelected>>", lambda event: self.update_trans_window(event, profile))

        # Clear the transaction window.
        self.clear_trans_window()

    def update_trans_window(self, event, profile):
        """ Event function bound to the account dropdown menu that calls
        the method to update the list of transactions when the value 
        of the dropdown changes. 
        """

        # Gets the selected account name from the combobox, associates
        # it with the correct account object, and calls the setup
        # function. 
        account_name = event.widget.get()
        account = profile.get_account_from_name(account_name)
        self.set_trans_window(account)

    def set_trans_window(self, account):
        """ Setup function that initializes a display for each 
        transaction in an account's list. 
        """
        
        self.clear_trans_window()

        # Frame for layout
        self.account_frame = tk.Frame(self.trans_region.interior)
        self.account_frame.pack(fill='x')

        # Setup a new account label
        self.account_label = tk.Label(self.account_frame, text=f"Account: {account.name}", font=('Arial', 12))
        self.account_label.pack(side='left', padx=30, pady=10, anchor='w')

        # Set an edit account button
        self.edit_account_button = tk.Button(self.account_frame, text="Edit Account", font=('Arial', 12), command=lambda: self.edit_account(account))
        self.edit_account_button.pack(side='right', padx=50, pady=10, anchor='e')

        # Setup the account balance label
        self.account_balance = tk.Label(self.account_frame, text=f"${account.balance:.2f}", font=('Arial', 12))
        self.account_balance.pack(side='right', padx=40, pady=10, anchor='e')

        # Setup display objects for each transaction in the list.
        for transaction in account.transactions:
            TransactionDisplay(self.trans_region.interior, transaction, self)

        # Add Transaction button.
        self.add_trans_button = tk.Button(self.trans_region.interior, text="Add Transaction", font=('Arial', 12), command=lambda: self.add_trans(account))
        self.add_trans_button.pack(side='bottom', anchor='w', padx=15, pady=15)

    def clear_trans_window(self):
        """ Clears all objects currently in the transaction display
        region. 
        """
        # Destroy all previous children of the frame object. 
        for child in self.trans_region.interior.winfo_children():
            child.destroy()

    def render_new_trans(self, trans):
        """ Method to add a new TransactionDisplay object to the list
        when a new transaction is added to the active account. Also
        updates the account balance label to match the new account
        balance.
        """

        TransactionDisplay(self.trans_region.interior, trans, self)
        self.account_balance.config(text=f"${trans.account.balance:.2f}")

    def add_account(self, profile):
        """ Method to be bound to the Add Account button, initializes
        a new instance of the AddAccountGUI class to open that GUI and 
        input info for a new account. 
        """

        AddAccountGUI(self, profile)
        

    def edit_account(self, account):
        """ Method bound to the Edit Account button, opens the Add 
        Account GUI window with prepopulated values and changes the 
        save method to edit the existing account. 
        """

        edit_window = AddAccountGUI(self, None)
        edit_window.setup_as_edit(account, self)


    def add_trans(self, account):
        """ Method to be bound to the Add Transaction button, 
        initializes a new instance of the AddTransactionGUI class to 
        open that GUI and input info for a new transaction. 
        """

        AddTransactionGUI(self.root, account, self.render_new_trans)

    def update_account_info(self, account):
        """ Updates the options in the account dropdown object after
        a change has been made to the options. 
        """

        self.account_selector.config(values=account.profile.get_account_names())

        # Update the account name label and account balance label.
        self.account_label.config(text=f"Account: {account.name}")
        self.account_balance.config(text=f"${account.balance:.2f}")

    def update_account_info_from_deletion(self, profile):
        """ Updates the options in the account dropdown object after
        an account has been deleted, and clears all the displayed info. 
        """

        self.account_selector.config(values=profile.get_account_names())

        # Clears the selection to prevent errors in case of deletion.
        self.account_selector.set('')
        for child in self.trans_region.interior.winfo_children():
            child.destroy()

class InputGUIParent:
    """ A parent class for the Add__GUI classes that contains a few
    helpful validation functions that each uses. 
    """

    def validate_entry_name(self, input):
        """ Method to be bound to a tk.Entry key input to ensure that
        all characters entered are permissible in a name. 
        """

        valid_input = True

        # Verify that all characters are valid 
        permissible_chars = ' -.!&#$%():'
        for char in input:
            if not char.isalnum() and not char in permissible_chars:
                valid_input = False

        return valid_input
            
    def validate_entry_money_value(self, input):
        """ Method to be bound to a tk.Entry key input to ensure that
        all characters entered are permissible in a money value. 
        """

        valid_input = True

        # Verify that all characters are valid 
        permissible_chars = '0123456789-.'
        for char in input:
            if char not in permissible_chars:
                valid_input = False
            
        # Ensure that there are not more than two decimal points.
        if '.' in input:
            for index, char in enumerate(input):
                if char == '.' and input.index('.') != index:
                    valid_input = False

        # Ensure that there are not more than two digits after the 
        # decimal place.
        if '.' in input:
            if len(input) > input.index('.') + 3:
                valid_input = False
        
        # Ensure that there are not more than two negative symbols.
        if '-' in input:
            for index, char in enumerate(input):
                if char == '-' and input.index('-') != index:
                    valid_input = False

        # Ensure that if there is a negative symbol that it is at the 
        # front.
        if '-' in input:
            for index, char in enumerate(input):
                if char == '-' and index != 0:
                    valid_input = False

        return valid_input

class AddAccountGUI(InputGUIParent):
    """ A Class to handle the details of the separate window opened when
    adding an additional account to a profile. 
    """

    def __init__(self, parent, profile):

        # Initialize new GUI window.
        self.root = tk.Toplevel(parent.root)
        self.root.wm_transient(parent.root)
        self.root.grab_set()
        self.root.geometry('600x300')
        self.root.title("Account Details")

        # Register methods for input validation.
        valid_name = self.root.register(self.validate_entry_name)
        valid_money = self.root.register(self.validate_entry_money_value)

        # Account name input.
        self.name_label = tk.Label(self.root, text="Account name:", font=('Arial', 12))
        self.name_label.pack(padx=20, pady=20)
        self.name_input = tk.Entry(self.root, font=('Arial', 12), validate='key', validatecommand=(valid_name, '%P'))
        self.name_input.pack(padx=20, pady=10)

        # Account balance input.
        self.balance_label = tk.Label(self.root, text="Account balance:", font=('Arial', 12))
        self.balance_label.pack(padx=20, pady=20)
        self.balance_input = tk.Entry(self.root, font=('Arial', 12), validate='key', validatecommand=(valid_money, '%P'))
        self.balance_input.pack(padx=20, pady=10)

        # Cancel button. 
        self.cancel_button = tk.Button(self.root, text="Cancel", font=('Arial', 10), command=self.close_add_account_window)
        self.cancel_button.pack(side='left', padx=10, pady=10, anchor='s')

        # Save button.
        self.save_button = tk.Button(self.root, text="Save", font=('Arial', 10), command=lambda: self.save_account_new(profile, parent))
        self.save_button.pack(side='right', padx=10, pady=10, anchor='s')

    def close_add_account_window(self):
        """ Closes the add account GUI window and returns control to
        the main GUI window. 
        """
        self.root.destroy()

    def save_account_new(self, profile, parent):
        """ Saves the entered data into a new account object and adds
        it to the profile. Also closes the GUI window. 
        """

        # Verify that input isn't empty:
        if self.name_input.get() == "" or self.balance_input.get() == "":
            return

        # Get the values.
        account_name = self.name_input.get()
        account_balance = float(self.balance_input.get())

        # Verify that the name doesn't already exist in another account.
        if account_name in profile.get_account_names():
            return

        # Create a new Account object in the profile.
        account = Account(account_name, account_balance)
        profile.add_account(account)

        # Set the account as the active account and update dropdown
        # options.
        parent.set_trans_window(account)
        parent.update_account_info(account)

        self.close_add_account_window()

    def setup_as_edit(self, account, parent):
        """ Repurposes the Add Account GUI window into an edit window by
        prepopulating the current values and modifying the save command.
        Also adds a delete button. 
        """

        # Prepopulate the current values.
        self.name_input.insert(0, account.name)
        self.balance_input.insert(0, f"{account.balance:.2f}")

        # Add a delete button
        self.delete_button = tk.Button(self.root, text="Delete", font=('Arial', 10), command=lambda: self.delete_account(account, parent.update_account_info_from_deletion))
        self.delete_button.place(relx=0.5, rely=1.0, y=-10, anchor='s')

        # Edit save command.
        self.save_button.config(command=lambda: self.save_account_edit(account, parent.update_account_info))

    def save_account_edit(self, account, option_update_func):
        """ Saves the data currently entered in the Add Account GUI as
        edits to the given account. Then closes the GUI window. 
        """

        # Verify that input isn't empty:
        if self.name_input.get() == "" or self.balance_input.get() == "":
            return

        # Verify that the name doesn't already exist in another account.
        if self.name_input.get() != account.name and self.name_input.get() in account.profile.get_account_names():
            return

        # Get the values and assign them to the account.
        account.name = self.name_input.get()
        account.balance = float(self.balance_input.get())

        # Update the options in the account selector dropdown and the
        # account labels.
        option_update_func(account)

        self.close_add_account_window()

    def delete_account(self, account, option_update_func):
        """ Method to be bound to the delete account button, asks for 
        confirmation from the user and then deletes the account from
        the profile. 
        """

        if messagebox.askyesno("Delete?", "Are you sure you wish to delete the " 
                             f"{account.name} account? This cannot be undone."):
            # User confirmed, now delete the account.
            account.profile.remove_account(account)

            # Update the options in the account selector dropdown.
            option_update_func(account.profile)

            # Close the edit window.
            self.close_add_account_window()

class AddTransactionGUI(InputGUIParent):
    """ Class to contruct and manage the GUI window opened when adding
    a new transaction to an account or editing details of a 
    transaction. 
    """
    
    def __init__(self, parent, account, update_func):

        # Initialize new GUI window.
        self.root = tk.Toplevel(parent)
        self.root.wm_transient(parent)
        self.root.grab_set()
        self.root.geometry('600x480')
        self.root.title("Transaction Details")

        # Register methods for input validation.
        valid_name = self.root.register(self.validate_entry_name)
        valid_money = self.root.register(self.validate_entry_money_value)

        # Transaction description input.
        self.desc_frame = tk.Frame(self.root)
        self.desc_frame.pack(padx=10, pady=30, fill='x')
        self.desc_label = tk.Label(self.desc_frame, text="Transaction description:", font=('Arial', 12))
        self.desc_label.pack(padx=0, pady=5)
        self.desc_input = tk.Entry(self.desc_frame, width=50, font=('Arial', 12), validate='key', validatecommand=(valid_name, '%P'))
        self.desc_input.pack(padx=0, pady=5)

        # Transaction amount input.
        self.amount_frame = tk.Frame(self.root)
        self.amount_frame.pack(padx=10, pady=0, fill='x')
        self.amount_label = tk.Label(self.amount_frame, text="Transaction amount:", font=('Arial', 12))
        self.amount_label.pack(padx=0, pady=5)
        self.amount_input = tk.Entry(self.amount_frame, font=('Arial', 12), validate='key', validatecommand=(valid_money, '%P'))
        self.amount_input.pack(padx=0, pady=5)

        # Transaction date input.
        self.date_frame = tk.Frame(self.root)
        self.date_frame.pack(padx=10, pady=30, fill='x')
        self.date_label = tk.Label(self.date_frame, text="Transaction date:", font=('Arial', 12))
        self.date_label.pack(padx=0, pady=5)
        self.date_entry = DateInput(self.date_frame)
        self.date_entry.pack(padx=0, pady=5)

        # Transaction type input.
        self.type_frame = tk.Frame(self.root)
        self.type_frame.pack(padx=10, pady=0, fill='x')
        self.type_label = tk.Label(self.type_frame, text="Transaction type:", font=('Arial', 12))
        self.type_label.pack(padx=0, pady=5)
        self.type_selector = ttk.Combobox(self.type_frame, values=["Expense", "Income"], state="readonly", font=('Arial', 12))
        self.root.option_add("*TCombobox*Listbox*Font", ('Arial', 12)) 
        self.type_selector.pack(padx=0, pady=0)
        self.type_selector.set("Expense")

        # Cancel button. 
        self.cancel_button = tk.Button(self.root, text="Cancel", font=('Arial', 10), command=self.close_trans_window)
        self.cancel_button.pack(side='left', padx=10, pady=10, anchor='s')

        # Save button.
        self.save_button = tk.Button(self.root, text="Save", font=('Arial', 10), command=lambda: self.save_trans_new(account, update_func))
        self.save_button.pack(side='right', padx=10, pady=10, anchor='s')
    
    def save_trans_new(self, account, update_func):
        """ Saves the values entered in the add transaction window
        into a new Transaction object and adds it to the list in the 
        corresponding account. 
        """

        # Verify that the entry fields are not empty and that the date 
        # is valid.  
        if (self.desc_input.get == "" or self.amount_input.get() == "" or \
                self.date_entry.get() == None):
            return

        # Get the values.
        desc = self.desc_input.get()
        amount = float(self.amount_input.get())
        date = self.date_entry.get()
        type = TransType[self.type_selector.get().upper()]

        # Create a new Transaction object and add it to the account.
        trans = Transaction(amount, desc, date, type)
        account.add_trans(trans)

        # Add the new transaction to the rendered list.
        update_func(trans)

        # Close the transaction window
        self.close_trans_window()
    
    def close_trans_window(self):
        """ Closes the add transaction GUI window. Bound to the cancel button.
        """
        self.root.destroy()
    
    def setup_as_edit(self, trans, update_func, delete_func):
        """ Sets up the add transaction window to act as an edit window
        for an exisiting transaction. Prepopulates the fields with the
        current values, adds a delete button, and changes the command
        bound to the save button. 
        """

        # Prepopulate current values in the fields.
        self.desc_input.insert(0, trans.description)
        self.amount_input.insert(0, f"{trans.amount:.2f}")
        self.date_entry.set(trans.date)

        # Setup the type selector as un-editable
        self.type_selector.set(trans.type.name.title())
        self.type_selector.config(state='disabled', background='pink')

        # Add a delete button
        self.delete_button = tk.Button(self.root, text="Delete", font=('Arial', 10), command=lambda: self.delete_trans(trans, delete_func))
        self.delete_button.place(relx=0.5, rely=1.0, y=-10, anchor='s')

        # Update the save button command. 
        self.save_button.config(command=lambda: self.save_trans_edit(trans, update_func))

    def save_trans_edit(self, trans, update_func):
        """ Saves the changes made to the transaction in the edit trans
        window. 
        """

        # Verify that the entry fields are not empty and that the date 
        # is valid.  
        if (self.desc_input.get == "" or self.amount_input.get() == "" or \
                self.date_entry.get() == None):
            return

        # Get the values.
        desc = self.desc_input.get()
        amount = float(self.amount_input.get())
        date = self.date_entry.get()

        # Update the values in the transaction. 
        trans.description = desc
        trans.date = date
        if trans.amount != amount:
            trans.update_amount(amount)

        # Update the transaction display tile. 
        update_func(trans)

        # Close the transaction window
        self.close_trans_window()

    def delete_trans(self, trans, delete_func):
        """ Deletes the given transaction from its account. 
        """

        # Remove the transaction from its account object.
        trans.account.remove_trans(trans)

        # Remove the display tile from the GUI window
        delete_func()

        # Close the transaction window
        self.close_trans_window()

class TransactionDisplay:
    """ A class to setup the display section for an individual
    transaction. 
    """

    def __init__(self, parent, trans, main_gui):

        # Store a reference to the main GUI window
        self.main_gui = main_gui

        # Frame to hold everything in.
        self.wrapper = tk.Frame(parent, borderwidth=3, relief=tk.RIDGE)
        self.wrapper.pack(padx=5, pady=2, fill='x')

        # Date label
        self.date_label = tk.Label(self.wrapper, text=f"{trans.date:%d %b %Y}", font=('Arial', 12))
        self.date_label.pack(side='left', padx=5, pady=5)

        # Description label
        self.desc_label = tk.Label(self.wrapper, text=f"{trans.description}", font=('Arial', 10))
        self.desc_label.pack(side='left', padx=5, pady=5, fill='x')

        # Edit button
        self.edit_button = tk.Button(self.wrapper, text="Edit", font=('Arial', 10), command=lambda: self.edit_trans(trans))
        self.edit_button.pack(side='right', padx=5, pady=5, anchor='ne')

        # Amount label
        self.amount_label = tk.Label(self.wrapper, text=f"${trans.amount:.2f}", font=('Arial', 12))
        self.amount_label.pack(side='right', padx=5, pady=5)

        # Expense vs Income differences
        if trans.type == TransType.EXPENSE:
            self.amount_label.config(fg='red')
        else:
            self.amount_label.config(fg='green')

    def update_values(self, trans):
        """ Method to populate new values into labels after an edit to
        transaction details. 
        """

        self.date_label.config(text=f"{trans.date:%d %b %Y}")
        self.desc_label.config(text=f"{trans.description}")
        self.amount_label.config(text=f"${trans.amount:.2f}")

        self.main_gui.account_balance.config(text=f"{trans.account.balance:.2f}")

    def delete(self, trans):
        """ Destroys the self.wrapper object to remove the GUI frame
        from the window. 
        """

        self.wrapper.destroy()

        self.main_gui.account_balance.config(text=f"{trans.account.balance:.2f}")

    def edit_trans(self, trans):
        """ Method to open the add transaction window for editing the
        given transaction. 
        """

        window = AddTransactionGUI(self.wrapper.winfo_toplevel(), None, None)
        window.setup_as_edit(trans, self.update_values, lambda: self.delete(trans))

class DateInput(ttk.Frame):
    """ A custom class written to allow the user to enter a date. Uses
    an Entry field to allow the user to enter the date, and buttons on
    either side to allow incrementing the date one day in either 
    direction.      %d %b %Y
    """

    # Constant used for validating date input. 
    VALID_DATE_CHARS = [
        "01",
        "0123456789",
        "/",
        "0123",
        "0123456789",
        "/",
        "12",
        "8901",
        "0123456789",
        "0123456789",
    ]

    def __init__(self, parent, default_date=date.today(), *args, **kw):

        # Call the parent frame init method. 
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Setup the increment and decrement buttons.
        self.decrement_button = tk.Button(self, text="<", command=lambda: self.increment_date(-1))
        self.decrement_button.pack(side='left', anchor='w')
        self.increment_button = tk.Button(self, text=">", command=lambda: self.increment_date(1))
        self.increment_button.pack(side='right', anchor='e')
        
        # Store the default background color and date.
        self.default_bg = parent.cget("bg")
        self.default_date = f"{default_date:%m/%d/%Y}"

        # Setup the entry field
        self.date_entry = tk.Entry(self, font=('Arial', 12), width=12, validate='all', validatecommand=(self.register(self.validate_entry_date), '%V', '%P'))
        self.date_entry.pack(padx=2, pady=5, fill='x', side='top', anchor='center')
        self.date_entry.insert(0, self.default_date) 

    def get(self):
        """ Returns the current value of the Entry field as a Date 
        object. If the current entered date is not a valid date, instead
        returns None. 
        """

        try:
            return datetime.strptime(self.date_entry.get(), "%m/%d/%Y").date()
        except ValueError:
            return None

    def set(self, date):
        """ Takes a date object and sets the entry field to represent
        that date. 
        """

        self.default_date = f"{date:%m/%d/%Y}"
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, self.default_date)
        self.date_entry.config(validate='all')

    def increment_date(self, offset):
        """ Sets the value of self.date_entry to the day after the 
        one it currently holds. Only executes if the current entry is
        a valid date. 
        """

        # Get current date value
        date_str = self.date_entry.get()

        # Confirm it is a valid date before continuing
        if DateInput.is_valid_date(date_str):

            # Turn the string into a datetime object and use timedelta
            # to increment it by the offset. 
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            date_delta = timedelta(days=offset)
            date_obj = date_obj + date_delta

            # Convert the date back into a string and update the entry
            # text. 
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, f"{date_obj:%m/%d/%Y}")

            # Turn back on entry validation after calling delete()
            self.date_entry.config(validate='all')


    def validate_entry_date(self, reason, input):
        """ Validation method to be bound to the self.date_entry field
        to not allow invalid date inputs. 
        """

        is_valid = True

        # Only actually validate anything on a keypress or focusout.
        if reason == 'focusout' or reason == 'key':
            
            # Verify that the string is not longer than allowed.
            if len(input) > 10:
                is_valid = False
            else:
                # Verify that all characters match valid options for the index.
                for index, char in enumerate(input):
                    if char not in self.VALID_DATE_CHARS[index]:
                        is_valid = False
        
        # Checks to run only if reason is focusout.
        if reason == 'focusout':  

            # if the input isn't valid, then turn the background pink 
            # if the input isn't valid, then turn the background pink
            # and reset the date to the default.
            if not DateInput.is_valid_date(input):
                self.date_entry.config(bg='pink')
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, self.default_date)

                # Turn back on validation after calling delete() and 
                # focus the cursor on the entry field. 
                self.date_entry.config(validate='all')
                self.date_entry.focus_set()

                is_valid = False

        if reason == 'key':
            # Always reset the background color on keypress.
            self.date_entry.config(bg='white')

        return is_valid 

    @staticmethod
    def is_valid_date(date):
        """ Takes a string representing a date and determines if it is
        valid. 
        """

        try:
            datetime.strptime(date, "%m/%d/%Y")
            is_valid = True
        except ValueError:
            is_valid = False

        return is_valid

class VerticalScrolledFrame(ttk.Frame):
    """ A class implementing a vertical scroll window. Borrowed off of 
    the internet. 

    Source: 
    https://gist.github.com/JackTheEngineer/
    81df334f3dcff09fd19e4169dd560c59
    """

    def __init__(self, parent, *args, **kw):

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        # Windows-specific mousewheel binding.
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        interior.bind('<Configure>', _configure_interior)
        canvas.bind('<Configure>', _configure_canvas)
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)