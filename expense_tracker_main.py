from expense_tracker_data import *
from expense_tracker_gui import ExpenseTrackerGUI
from tkinter import messagebox, simpledialog, filedialog
import pickle, shelve

"""
Welcome to the Expense Tracker. This program uses a GUI window to allow
a user to personally track their financial account information in one
place to verify that the expected amounts match the actual amounts.

This program is organized into four files - this file contains the 
control portion and the save/load portions, expense_tracker_gui.py 
contains all of the GUI control portions, expense_tracker_data.py 
contains the classes used for data representation, and 
test_expense_tracker.py contains all of the testing functions. 

Note that due to a limitation in the VertialScrolledFrame class, 
there may be some odd scroll behavior on Linux and Mac systems. 
"""

class Controller:
    """ Class to handle program control and store program data.
    """

    # Constant to store filepath to persistent app data. 
    APP_DATA_FILEPATH = "appdata.pk"

    def __init__(self):
        """ Initailzer for the class, serves as the main program
        control function. 
        """

        # Read current file path from persistent data shelf. 
        with shelve.open(self.APP_DATA_FILEPATH) as db:
            if "active_filepath" in db:
                self.active_file_path = db["active_filepath"]
            else:
                self.active_file_path = None

        # If we have an active filepath, attempt to read the object 
        # there.
        if self.active_file_path != None:
            try:
                self.active_profile = self.load_from(self.active_file_path)
            except (FileNotFoundError, pickle.UnpicklingError):
                # If the file doesn't exist or isn't valid, reset the 
                # active filepath and active profile.
                self.active_file_path = None
                self.active_profile = None
        else:
            # If there is no active filepath, initialize the active 
            # profile to None.
            self.active_profile = None

        # Create an ExpenseTrackerGUI object to intialize the GUI. Note
        # that since this starts the tkinter infinite loop, program
        # flow will never return here.
        ExpenseTrackerGUI(self, self.active_profile)

    def new_profile(self):
        """ Asks if the user wants to save the current profile if one 
        is open, then prompts the user for the name of a new profile
        and creates it. 
        """

        # If there is a profile currently active, ask if the user wants
        # to save it before continuing. 
        if self.active_profile != None:
            if messagebox.askyesno("Save?", "Would you like to save the "\
                                   "current profile before continuing?"):
                self.save()

        # Prompt for a new profile name. 
        user_input = simpledialog.askstring("Profile Name", 
                                            "Enter a name for the new profile:", 
                                            initialvalue="New Profile")

        if user_input != None:

            # If the profile name is empty, just display a "creation 
            # failed" message
            if user_input == "":
                messagebox.showerror("Invalid", 
                                     "Invalid name, profile creation failed")
            else:
                # Create a new profile and update the GUI to match. 
                self.active_profile = Profile(user_input)
                self.main_gui.setup_profile_in_gui(self.active_profile)
                messagebox.showinfo("Success", 
                                    "New profile successfully created!")

                # Also reset the active filepath.
                self.active_file_path = None

    def load(self):
        """ Prompts the user to select a file and attempts to load a
        Profile object from it. 
        """

        # If there is a profile currently active, ask if the user wants
        # to save it before continuing. 
        if self.active_profile != None:
            if messagebox.askyesno("Save?", 
                                   "Would you like to save the current "\
                                    "profile before continuing?"):
                self.save()

        # Prompt the user for a filepath.
        load_filepath = filedialog.askopenfilename()

        try:
            # Load data and update variables.
            self.active_profile = self.load_from(load_filepath)
            self.active_file_path = load_filepath

            # Update GUI after successfully loading
            self.main_gui.setup_profile_in_gui(self.active_profile)

        except (FileNotFoundError, pickle.UnpicklingError):
            # Error message if load fails.
            messagebox.showerror("Load Error", "Unable to open that file")

    def load_from(self, filepath):
        """ Attempts to load and return a Profile object from the file 
        at filepath. Does not handle any exceptions, they should be 
        handled by higher-level functions. 
        """

        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def save_and_exit(self):
        """ If a profile is currently active, saves it and exit the 
        program.
        """
        
        if self.active_profile != None:
            self.save()
        
        self.exit()

    def save(self):
        """ Saves the currently active profile to its file. If a 
        filepath for it isn't stored, prompts the user to select one
        and then saves the profile to that file. 
        """

        if self.active_file_path == None:
            self.save_as_new_profile()
        else:
            self.save_to(self.active_file_path)
    
    def save_as_new_profile(self):
        """ Prompts the user to enter a filepath, then saves the 
        currently active profile to that file. 
        """
        
        # Prompt the user for a filepath and append a file extension.
        save_filepath = filedialog.asksaveasfilename()
        save_filepath += ".etpk"

        # Save to the filepath.
        self.save_to(save_filepath)

    def save_to(self, filepath):
        """ Saves the currently active profile to the given filepath.
        """

        # Save the profile object.
        with open(filepath, 'wb') as file:
            pickle.dump(self.active_profile, file)

        # Update the current active filepath.
        self.active_file_path = filepath

    def exit_confirm(self):
        """ Confirm that the user wishes to exit, then close the 
        program.
        """
        if messagebox.askyesno("Quit?", "Are you sure you wish to quit? Any " \
                               "unsaved progress will be lost."):
            self.exit()

    def exit(self):
        """ Closes the program with no questions asked.   
        """

        # Store current file path to persistent data shelf. 
        with shelve.open(self.APP_DATA_FILEPATH) as db:
            db["active_filepath"] = self.active_file_path

        self.main_gui.root.destroy()

if __name__ == "__main__":
    # Initialize the Controller object to begin program execution. 
    Controller()