# imports

import tkinter
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from pathlib import Path
import time


# Constants

casinoGames = ["Blackjack", "Poker", "Dice"]
WINDOOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = "#1d1d1d"
DEBUG = False


# Initalize the client class ### Maybe allowing for multiplayer? only lan with ports?

class Client:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Casino")
        self.root.geometry(f'{WINDOOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.root.configure(background=BACKGROUND_COLOR)


    # Closing Manager

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


    # Auth Manages the login and registration of the user as well as the modal.

    def auth(self):


        # Modal Frame creation

        self.logInModal = tkinter.Toplevel(self.root)
        self.logInModal.title("Log In")
        self.logInModal.geometry('360x240')
        self.logInModal.resizable(False, False)
        self.logInModal.configure(background=BACKGROUND_COLOR)
        self.logInModal.wm_attributes("-topmost", 0)
        self.userData = {}


        # Login warning on the main screen. Telling the user to log in incase modal doesnt appear.

        tkinter.Label(self.root, text="Please log in first, if you do not see a log in box \nplease close the program and reopen it.", bg=BACKGROUND_COLOR, fg='#ffffff', font=('Helvetica', 24)).grid(row=0, column=0, sticky='nesw')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)


        # Hide the main menu screen and adds custom closing manager.

        self.root.iconify()
        self.logInModal.protocol("WM_DELETE_WINDOW", self.on_closing)


        # Warning func - simple only 1 pram

        def warning(message):
            warn = tkinter.Label(self.logInModal, text=message, bg='red', fg='#fff',border=5, relief="raised", font=('Helvetica', 8), padx=10, pady=10)
            warn.grid(row=5, column=0, sticky='ew', padx=20, columnspan=2)

        
        # Func to find what widget has focus, and set it apart if its a text box.

        def focus(event):
            widget = self.logInModal.focus_get()
            widget.configure(relief="solid", borderwidth=2, bg='#fff', fg='#000')
            for child in self.logInModal.winfo_children():
                if child != widget and child.winfo_class() == "Entry":
                    child.configure(relief="groove", borderwidth=1, bg=BACKGROUND_COLOR, fg='#fff')


        # Func to check if the user has entered a valid username and password. 
        # TODO: Hash the password. 

        def checkLogin(username, password):
            if not username or not password:
                warning( "Please fill in all fields")
            else:
                with open("data\mydata.json", 'r') as f:
                    for user in json.load(f):
                        if user['username'] == username and user['password'] == password:
                            print("Found user")
                            self.userData = user
                            self.logInModal.destroy()
                            for child in self.root.winfo_children():
                                child.destroy()
                            self.mainMenu()
                            self.root.deiconify()
                            
                            return
                        else:
                            warning("Username or password is incorrect. Try again")
                

        # Func to create a new user, and add it to the data file, if all fields are valid and not taken.

        def createAccount(username, password, confirmPassword):
            if not username or not password or not confirmPassword:
                warning("Please fill in all fields")
            elif password != confirmPassword:
                warning("Passwords do not match")
            else:
                with open("data\mydata.json", 'r') as f:
                    for user in json.load(f):
                        if user['username'] == username:
                            warning("Account with that name already exists")
                            return
                    with open("data\mydata.json", 'r+') as f:
                        data = json.load(f)
                        data.append({
                                        #Template user
                                        "UserID": (int(data[-1]['UserID'])) + 1,
                                        "username": username,
                                        "password": password,
                                        "balance": 100,
                                        "ProfilePicture": "images/default.jpg"
                                        })
                        f.seek(0)
                        json.dump(data, f)
                        # time.sleep(0.1)  # add a delay to make sure the file is written. Seems to not need anymore?
                checkLogin(username, password) 

        
        #Creating all the widgets for the login and registration modal.


        # Username Label and Entry Creation

        userNameLabel = tkinter.Label(self.logInModal, text="Username: ", bg=BACKGROUND_COLOR, fg='#fff')
        userNameEntry = tkinter.Entry(self.logInModal,  bg='#1d1d1d', fg='#fff', relief="groove" )
        

        # Password Label and Entry Creation

        passwordLabel = tkinter.Label(self.logInModal, text="Password: ", bg=BACKGROUND_COLOR, fg='#fff')
        passwordEntry = tkinter.Entry(self.logInModal,show="*", bg=BACKGROUND_COLOR, fg='#fff') 


        # Username Label and Entry placement

        userNameLabel.grid(row=0, column=0, sticky='ew', pady=10)
        userNameEntry.grid(row=0, column=1, sticky='we', padx=20, pady=10)


        # Password Label and Entry placement

        passwordLabel.grid(row=1, column=0, sticky='ew', pady=10 )
        passwordEntry.grid(row=1, column=1, sticky='we',  padx=20,pady=10 )


        # Grid Configure for modal

        self.logInModal.columnconfigure(0, weight=1)
        self.logInModal.columnconfigure(1, weight=1)


        # Login Button Creation and placement

        loginButton = tkinter.Button(self.logInModal, text="Login", command=lambda: checkLogin(userNameEntry.get(), passwordEntry.get()))
        loginButton.grid(row=3, column=0, sticky='ew', padx=20, pady=10, columnspan=2)

        
        # Register Button Creation and placement
        
        CreateAccountButton = tkinter.Button(self.logInModal, text="Create New Account", command=lambda: switch_to_create_accont() )
        CreateAccountButton.grid(row=4, column=0, sticky='ew', padx=20, pady=10, columnspan=2)


        # Confirm Password Label and Entry Creation

        confirmPasswordLabel = tkinter.Label(self.logInModal, text="Confirm Password: ", bg=BACKGROUND_COLOR, fg='#fff')
        confirmPasswordEntry = tkinter.Entry(self.logInModal, show="*", bg=BACKGROUND_COLOR, fg='#fff')

        
        # Function to switch to the create account screen.

        def switch_to_create_accont():
            # Change title and size of the modal.

            self.logInModal.title("Create Account")
            self.logInModal.geometry('400x260')


            # Change the text and actions of the buttons.

            loginButton.config(text="Create & Login", command=lambda: createAccount(userNameEntry.get(), passwordEntry.get(), confirmPasswordEntry.get()))
            CreateAccountButton.config(text="Already Have an account? Sign In", command=lambda: switch_to_login())


            # Show the previously made confirm password label and entry.

            confirmPasswordLabel.grid(row=2, column=0, sticky='ew', pady=10)
            confirmPasswordEntry.grid(row=2, column=1, sticky='we', padx=20, pady=10)


        # Function to switch back to the login screen.
       
        def switch_to_login():
            # Change title and size of the modal.

            self.logInModal.title("Log In")
            self.logInModal.geometry('360x240')


            # Change the text and actions of the buttons.

            loginButton.config(text="Login", command=lambda: checkLogin(userNameEntry.get(), passwordEntry.get()))
            CreateAccountButton.config(text="Create New Account", command=lambda: switch_to_create_accont())


            # Hide the previously made confirm password label and entry. BUT keep grid placement.

            confirmPasswordLabel.grid_remove()
            confirmPasswordEntry.grid_remove()

        
        # Binding the focus event to mouse click.

        self.logInModal.bind_all("<Button-1>", lambda event: focus(event))
        
        
    # Function to create the main menu.

    def mainMenu(self):
        profilePic = Image.open(self.userData['ProfilePicture'])
        pic = profilePic.resize((75,75), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(pic)
        # Creation and placement of the sidebar frame.

        self.sideBarFrame = tkinter.Frame(self.root, height=WINDOW_HEIGHT,relief='sunken', borderwidth=1) #maybe width 200
        self.sideBarFrame.grid(row=0, column=0, sticky='nesw')
        

        # Creation and placement of the main frame

        self.mainMenuFrame = tkinter.Frame(self.root, bg='#1d1d1d')
        self.mainMenuFrame.grid(row=0, column=1, sticky='nesw')


        # Column and Row config for the main screen

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=8)
        self.root.rowconfigure(0, weight=1)

        
        # Column and Row config for the sidebar

        self.sideBarFrame.columnconfigure(0, weight=1)
        self.sideBarFrame.columnconfigure(1, weight=1)
        self.sideBarFrame.columnconfigure(2, weight=1)
        self.sideBarFrame.columnconfigure(3, weight=0)
        self.sideBarFrame.rowconfigure(2, weight=1)


        userNameLabel = tkinter.Label(self.sideBarFrame, text=f'Welcome, \n{self.userData["username"]}',font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg='#fff')
        userNameLabel.grid(row=0, column=0, sticky='new', columnspan=3,pady=20, padx=20)


        profilePic = tkinter.Button(self.sideBarFrame ,image=pic, command=lambda: print(self.userData['username']), pady=10,)
        profilePic.image = pic
        profilePic.grid(row=1, column=1, sticky='n',)



        chipCounter = tkinter.Label(self.sideBarFrame, text=f'Chips: {self.userData["balance"]}',)
        chipCounter.grid(row=2, column=0, padx=20, columnspan=3, sticky='new', pady=10)

        














        # Quit Button Creation and placement

        QuitButton = tkinter.Button(self.sideBarFrame, text="Quit", command=self.on_closing, )
        QuitButton.grid(row=3, column=0, sticky='sew', padx=10, pady=10, columnspan=3)





































    # Func to start client. Starts auth first.

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        if not DEBUG:
            self.auth()
        else:
            self.userData = {'username': 'testing', 'password': 'test', "balance": 999, "ProfilePicture": "images/MMLogo2.png"}
            self.mainMenu()

        self.root.mainloop()




# Just making test client and running it.
#TODO: Could be turned into multiplayer. would need to move processing to server script.

h = Client()
h.run()
