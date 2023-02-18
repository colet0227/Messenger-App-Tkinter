
# FINAL PROJECT
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.
# Name: Nathan Yang, Cole Thompson
# Email: npyang@uci.edu, cwthomps@uci.edu
# ID: 63942782, 36762668
from ast import JoinedStr
from operator import index
from textwrap import fill
import tkinter as tk
from tkinter import Y, ttk, filedialog
from Profile import Post, Profile
import ds_messenger as DM
from datetime import datetime
import time


class FileNotCreated(Exception):
    """
    FileNotCreated is a custom exception handler that is raised when 
    attempting to close a new file after it has not been created.
    """
    pass


class FileNotOpened(Exception):
    """
    FileNotOpened is a custom exception handler that is raised when 
    attempting to close an existing file after it has not been loaded.
    """
    pass


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._messages = []
        self._recipients = []
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def node_select(self, event):
        """
        Loads the previous messages assigned to the selected user in the
        display frame when the corresponding node in the posts_tree is selected. 
        """
        self.display.delete(0, tk.END)
        it = self.posts_tree.focus()
        # x is the name of the user that is being clicked on
        global x
        x = self.posts_tree.item(it)['text']
        try:
            # Runs if the user is creating a new file and loads an existing profile
            if new_save == 1:
                # Iterates through a list of dictionaries to insert previous messages that are from "x"
                for val in new2_list:
                    try:
                        self.display.insert(tk.END, val[x])
                    except:
                        pass
        except:
            pass
        try:
            # Runs if the user is loading an existing profile
            if old_save == 1:
                # Iterates through a list of dictionaries to insert previous messages that are from "x"
                for val in all_list:
                    try:
                        self.display.insert(tk.END, val[x])
                    except:
                        pass
        except:
            try:
                # Runs if the user is not connected to the internet
                if offline == 1:
                    # Iterates through a list of messages to insert previous messages that are from "x"
                    for obj in offline_list:
                        char_index = obj.index(": ")
                        user_str = obj[:char_index]
                        if x == user_str:
                            try:
                                self.display.insert(tk.END, obj)
                            except:
                                pass
            except:
                pass
        self.display.insert(tk.END, "\n")

    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """
        return self.entry.get('1.0', 'end-1c').rstrip()

    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        This method is useful for clearing the widget.
        """
        self.entry.delete(0.0, 'end')
        self.entry.insert(0.0, text)

    def set_posts(self, recipients:list):
        """
        Populates the self._posts attribute with posts from the active DSU file.
        """
        self._recipients = recipients
        rec_length = len(self._recipients) - 1
        for val in self._recipients:
            self._insert_post_tree(rec_length, val)

    def insert_post(self, post: Post):
        """
        Inserts a single post to the post_tree widget.
        """
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)
    
    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.set_text_entry("")
        self.entry.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _insert_post_tree(self, id, recipient):
        """
        Inserts a post entry into the posts_tree widget.
        """
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widgetz
        entry = recipient
        if len(entry) > 25:
            entry = entry[:24] + "..."
        self.posts_tree.insert(parent='', index = id, text=entry)
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # Post Frame Widget
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        # Post Tree Widget
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        
        # Display Listbox Widget
        self.display = tk.Listbox(master=self, height =10)
        self.display.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        for val in self._messages:
            self.display.insert(tk.END, val.get_entry())
        self.display.insert(tk.END, "Enter Settings in the Menu Bar to edit/create a username and password.")
        
        # Text Box Widget
        self.entry = tk.Text(master=self, height=5)
        self.entry.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, pady = 10)
        
        # Scrollbar Widget
        scrollbar = tk.Scrollbar(master=self.display)
        self.display['yscrollcommand'] = scrollbar.set
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None, user_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._user_callback = user_callback

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()

    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            try:
                self._save_callback()
            except:
                print("ERROR")

    def add_user(self):
        """
        Calls the callback function specified in the user_callback class attribute, if
        available, when the user_button has been clicked.
        """
        if self._user_callback is not None:
            self._user_callback()

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # Save/Send Button
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        
        # Footer Label
        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)
        
        # Add User button
        user_button = tk.Button(master=self, text="Add User", width=20)
        user_button.configure(command=self.add_user)
        user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)


class DarkMode(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for switching between the light and dark mode for the text box and display box.
    """
    def __init__(self, root, entry, display, tree):
        """This initializes the root and sets the attributes."""
        tk.Frame.__init__(self, root)
        self.root = root
        self.entry = entry
        self.display = display
        self.tree = tree
        
        # This attribute checks whether the toggle for dark mode is on/off
        self.is_on = False
        
        # The draw function will create the button and set it to the change command
        self._draw()
    
    def change(self):
        """This action will switch the theme to blue or black, depending on whether the is_on attribute is True or False."""
        if self.is_on:
            # This will change it to light mode with black text
            self.entry.configure(bg= "white", foreground = "black")
            self.display.configure(bg= "white", foreground = "black")
            self.is_on = False
        
        else:
            # This will change it to dark mode with white text
            self.entry.configure(bg= "black", foreground = "white")
            self.display.configure(bg= "black", foreground = "white")
            self.is_on = True
    
    def _draw(self):
        """The draw function here will create a new Toggle button to switch themes."""
        user_button = tk.Button(master=self, text="Toggle Dark Mode", width=20)
        user_button.configure(command=self.change)
        user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        pass


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class.
    """

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        
        # Initialize a new Profile and assign it to a class attribute.
        self._current_profile = Profile()
        self.new_list = []
        self.new2_list = []
        self.all_list = []
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

        # Profile filename
        self._profile_filename = None

    def check_something(self):
        """
        Tkinter Time Event to constantly check for new incoming messages.
        """
        self._current_profile = Profile()
        try:
            self._current_profile.load_profile(self._profile_filename)
        except:
            pass

        if (self._current_profile.username != None) and (self._current_profile.password != None):
            # Instantiates the DirectMessenger class
            dm2 = DM.DirectMessenger(dsuserver = "168.235.86.101", username = self._current_profile.username, password = self._current_profile.password)
            
            # Calls the DirectMessenger method retrieve_new()
            messages_list = dm2.retrieve_new()
            
            # Iterates through DirectMessage object list
            for val in messages_list:
                msg = val.recipient + ": " + val.message + "\tReceived: " + str(datetime.utcfromtimestamp(float(val.timestamp)))
                self.new_list.append({val.recipient: msg})
                self._current_profile.adding_messages(msg)
                self._current_profile.save_profile(self._profile_filename)
            
            # New_list variable will get all the new messages
            global new_list
            new_list = self.new_list
            
            # Iterates through list and the keys to check and see if the node that is selected is equivalent to the
            # user that has sent a recent message
            for val in new_list:
                for item in val.keys():
                    try:
                        if x == item:
                            # If the node selected and user are equivalent then the incoming message will be inserted into the display
                            self.body.display.insert(tk.END, val[x])
                    except:
                        pass
                try:
                    # If all_list exists then the val will also be appended to it
                    all_list.append(val)
                except:
                    pass
        else:
            pass
        
        # Resets the list for recent incoming messages
        self.new_list = []
        
        # Recalls the method
        self.after(5000, self.check_something)    
        
    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        try:
            filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name
            self._current_profile = Profile()
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
        except:
            # Custom exception
            raise FileNotCreated()    
 
    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        try:
            self._profile_filename = filename.name
        except:
            # Custom Exception
            raise FileNotOpened()
        
        # This will create a profile object and then load it with the file the user selects after hitting the open button
        self._current_profile = Profile()
        self._current_profile.load_profile(self._profile_filename)
        self.body.set_posts(self._current_profile.recipients)
        
        try:
            # Instantiates the DirectMessenger class if Internet is on
            dm2 = DM.DirectMessenger(dsuserver = "168.235.86.101", username = self._current_profile.username, password = self._current_profile.password)
            
            # Calls the DirectMessenger method retrieve_all()
            messages_list = dm2.retrieve_all()
            
            # Iterates through DirectMessage object list
            for obj in messages_list:
                msg = obj.recipient + ": " + obj.message + "\tReceived: " + str(datetime.utcfromtimestamp(float(obj.timestamp)))
                self.all_list.append({obj.recipient: msg})
                self._current_profile.adding_messages(msg)
                self._current_profile.save_profile(self._profile_filename)
            
            global all_list
            # List of all receive messages
            all_list = self.all_list
            
            global old_save
            old_save = 1
        except:
            # If the internet is off
            global offline_list
            
            # List of profile messages
            offline_list = self._current_profile.messages
            
            global offline
            offline = 1

    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    def save_profile(self):
        """Save a post entry when the user clicks the save_button widget to the active DSU file."""
        self._current_profile.save_profile(self._profile_filename)
        # Instantiates the DirectMessage class
        dm = DM.DirectMessage()
        
        try:
            dm.recipient = x
            sending = 1
        except:
            # If the user tries to send without clicking on a user
            self.body.display.insert(tk.END, "Please click on a user.")
            sending = 0
        
        if sending == 1:
            # Assings message atrribute to the text that is inputted in the text box
            dm.message = self.body.get_text_entry()
            # Insantiates the DirectMessenger class
            dm2 = DM.DirectMessenger(dsuserver = "168.235.86.101", username = self._current_profile.username, password = self._current_profile.password)
            # Calls the DirectMessenger method send() with the DirectMessage obj's message nad recipient as params
            dm2.send(dm.message, dm.recipient)
            clock = time.time()
            
            # Formats the message in a "username": "message"    Sent: "timestamp"
            msg = self._current_profile.username + ": " + dm.message + "\tSent: " + str(datetime.utcfromtimestamp(float(clock)))
            
            try:
                # Appends message along with the recipient to all_list so if the user goes to a different recipient and then back, 
                # the sent message will be in the display along with the received messages
                all_list.append({dm.recipient : msg})
            except:
                pass
            
            # New profile method
            self._current_profile.adding_messages(msg)
            self._current_profile.save_profile(self._profile_filename)
            
            # This will insert the message into the display and strip the text entry box of the message
            self.body.display.insert(tk.END, msg)
            self.body.entry.delete('1.0', tk.END)

    def add_user(self):
        """
        Creates widgets for adding a new user to send to when the Add User button is clicked in the footer.
        """
        self.new = tk.Tk()

        # Creates dimensions of the new add_usr window and titles it NEW USER
        self.new.geometry("250x250")
        self.new.title("NEW USER")
        
        # Notifies user to exit when done
        tk.Label(self.new, text="Please click Exit when done.").pack()
        
        # Username Label
        tk.Label(self.new, text="Username:", font=('Helvetica 17 bold')).pack(pady=20)
        
        # New User Entry
        self.text_field = tk.Entry(self.new)
        self.text_field.pack(pady=5)
        
        # Confirm Button
        confirm_button = tk.Button(master=self.new, text="Confirm", width=10, command=self.save_user)
        confirm_button.pack(pady=5)
        
        # Exit Button
        exit_button = tk.Button(self.new, text="Exit", command=self.new.destroy)
        exit_button.pack(pady=10)
            
    def save_user(self):
        """
        Saves inputted new users by getting the entry information. Saves to the profile as well as inputs the new users
        into the post tree. Method occurs wehn the Confirm button is clicked in the add_user method.
        """
        user = self.text_field.get()
        
        # New Profile method
        check = self._current_profile.adding_user(user)
        try:
            self._current_profile.save_profile(self._profile_filename)
        except:
            return
        
        if check == 1:
            self.body._insert_post_tree(len(self._current_profile.recipients) - 1, user)
        else:
            print("User has already been added.")
    
    def edit_profile(self):
        """
        Called when the Edit button is clicked within the cascade settings menu.
        Creates a new window of widgets for the user to input a username and password.
        """
        self.new2 = tk.Tk()
        
        # Creates a new edit profile window with these dimensions and labels it EDIT PROFILE
        self.new2.geometry("250x250")
        self.new2.title("EDIT PROFILE")
        
        # Notifies user to exit when done
        tk.Label(self.new2, text="Please click Exit when done.").pack()
        
        # Username Label
        tk.Label(self.new2, text="NEW USERNAME:", font=('Helvetica 10 bold')).pack(pady=5)
        
        # Username Entry
        self.new_username = tk.Entry(self.new2)
        self.new_username.pack(pady=5)
        
        # Password Label
        tk.Label(self.new2, text="NEW PASSWORD:", font=('Helvetica 10 bold')).pack(pady=5)
        
        # Password Entry
        self.new_password = tk.Entry(self.new2)
        self.new_password.pack(pady=5)
        
        # Confirm button
        confirm_button = tk.Button(master=self.new2, text="Confirm", width=10, command=self.edit_user)
        confirm_button.pack(pady=5)
        
        # Exit button
        exit_button = tk.Button(self.new2, text="Exit", command=self.new2.destroy)
        exit_button.pack(pady=10)

    def edit_user(self):
        """"
        Gets the information inputted into the username and password, then connects to the server to receive and previous messages
        when the user clicks on the Confirm button in the edit_profile method.
        """
        new_user = self.new_username.get()
        new_pass = self.new_password.get()
        self._current_profile.username = new_user
        self._current_profile.password = new_pass
        
        try:
            self._current_profile.save_profile(self._profile_filename)
            # Instantiates the DirectMessenger class
            dm2 = DM.DirectMessenger(dsuserver = "168.235.86.101", username = self._current_profile.username, password = self._current_profile.password)
            # Calls the DirectMesenger method retrieve_all()
            messages_list = dm2.retrieve_all()
            
            # Iterates through each DirectMessage object and appends it to the new2_list variable
            for obj in messages_list:
                # Formats the message object and appends it to the list
                msg = obj.recipient + ": " + obj.message + "\tReceived: " + str(datetime.utcfromtimestamp(float(obj.timestamp)))
                self.new2_list.append({obj.recipient: msg})
                
                # Adds the recipients to the current profile
                self._current_profile.recipients.append(obj.recipient)

                # Sorts the recipients so there are no duplicates
                x = set(self._current_profile.recipients)
                self._current_profile.recipients = list(x)

                # New Profile Method
                self._current_profile.adding_messages(msg)
                self._current_profile.save_profile(self._profile_filename)
            
            self.body.set_posts(self._current_profile.recipients)

            global new2_list
            # List of dictionaries with recipients as keys and messages as values
            new2_list = self.new2_list
            
            global new_save
            new_save = 1
        except:
            pass

    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        
        # Adds the cascading menu labeled File to the menu bar
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        # Adds the cascading menu labeled Settings to the menu bar
        menu_file2 = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file2, label='Settings')
        menu_file2.add_cascade(label = "Edit", command=self.edit_profile)
        menu_file2.add_command(label='Close', command=self.close)

        # Body Class intialization packed into the root window
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    
        # Footer Class initialization packed into the root window
        self.footer = Footer(self.root, save_callback=self.save_profile, user_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        # Dark Mode Class initialization packed into the root window
        self.body.entry.configure(bg= "white", foreground = "black")
        self.body.display.configure(bg= "white", foreground = "black")
        self.darkMode = DarkMode(self.root, self.body.entry, self.body.display, self.body.posts_tree)
        self.darkMode.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    main = tk.Tk() # Creates the interface
    main.title("Sliding into the DMs") # Establishes the title of the GUI
    main.geometry("720x480") # Establishes the dimensions of the main interface
    main.option_add('*tearOff', False)
    
    app = MainApp(main) # Assigned to app for Tkinter timer event
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    
    main.after(5000, app.check_something) # Tkinter timer event method call
    main.mainloop()
