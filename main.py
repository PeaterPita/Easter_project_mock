# imports

import tkinter
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from pathlib import Path
import math
import time
from tkinter.filedialog import askopenfilename
import random
import markdown
import webbrowser
import socket
import os






# Constants

casinoGames = ["BlackJack", "Roulette", "Dice", "Slot Machine"]
WINDOOW_WIDTH = 1000
WINDOW_HEIGHT = 600
MAX_LEVEL = 100


# COLORS
BACKGROUND_COLOR = "#1d1d1d" # dark gray  black
SECONDARY_BACKGROUND_COLOR = "#f5f5f5" #rayish white
FOREGROUND_COLOR = "#ffffff" # white
ACCENT_COLOR = "#6c0eed" # Purple



FONT = 'Helvetica'



# Initalize the client class ### Maybe allowing for multiplayer? only lan with ports?

class Client:

    



    # Initialize the client class

    def __init__(self):


        # Initialize the root window

        self.root = tkinter.Tk()
        self.root.title("Casino")
        self.root.geometry(f'{WINDOOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.root.configure(background=BACKGROUND_COLOR)
        self.BOOT_TIP = False





    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    tkinter.Canvas.create_circle = _create_circle


    def howToPlay(self, game):
        with open(f'Games/{game.split(" ")[0]}/HTP.md', 'r') as f:
            html = markdown.markdown(f.read())

        f = open('HTP.html', 'w')
        f.write(html)
        f.flush()

        webbrowser.open('HTP.html')

    def testConnection(self):
        try:
            s = socket.create_connection(('1.1.1.1', 80))
            s.close()
            return True
        except OSError:
            pass
        return False

    def launchGame(self, game):
        try:
            self.GameButton.configure(state="disabled", text=f'{game}\nNow Playing..')

            self.gameWindow = tkinter.Toplevel(self.root)
            self.gameWindow.title(game)
            self.gameWindow.geometry("900x700")
            self.gameWindow.resizable(False, False)
            self.gameWindow.configure(background=BACKGROUND_COLOR)


            def closeGame():
                if tkinter.messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
                    self.gameWindow.destroy()
                    self.GameButton.configure(state="normal", text=f'{game}')
                
            self.gameWindow.protocol("WM_DELETE_WINDOW", closeGame)





      

            eval(f'self.{game.split(" ")[0]}')



            
           
        
        except Exception as e:
            print(f'Failed to launch game {game}\n{e}')






    # Function to get the users profile pic. If the original file is not found, it will return the default profile pic.

    def getProfilePic(self):
        """getProfilePic - Returns the profile picture of the user as a ImageTk object. If the file is not found, it will return the default profile pic.

        Returns:
            ImageTk.PhotoImage: the profile picture as a ImageTk object. Resized to be 75x75.
        """

        try:
            profilePic = Image.open(self.userData['ProfilePicture'])
        except:
            print("Something went wrong when trying to get the profile picture. Restorted back to default")
            profilePic = Image.open("images/default.jpg")

        pic = profilePic.resize((75,75), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(pic)
        return pic


    # Function to get the focused widget. Currently only used to change entry so its more obvious what is being edited.

    def focus(self, parent):
        """focus - Changes the look of the focused widget. Currently only used to change entry so its more obvious what is being edited.

        Args:
            parent (Frame): The parent frame to check for focused widgets. 
        """

        widget = parent.focus_get()
        if isinstance(widget, tkinter.Entry):
            widget.configure(relief="solid", borderwidth=2, bg='#fff', fg='#000')
        for child in parent.winfo_children():
            # print(f'Child: {child}')
            if child != widget and child.winfo_class() == "Entry":
                child.configure(relief="groove", borderwidth=1, bg=BACKGROUND_COLOR, fg='#fff')


    # Function to validate wether the users password is acceptable. Used in create account and change password.

    def validatePassword(self, password):
        """validatePassword Checks the supplied password against the requirements.

        Args:
            password (str): the password the user has entered

        Returns:
            Tuple: A tuple containing wether the password is valid, and if it isnt the reason why.
        """


        if len(password) < 6:
            return (False, "Password must be at LEAST 6 characters long")
        elif password.isdigit():
            return (False, "Password must contain at LEAST one letter")
        elif password.isalpha():
            return (False, "Password must contain at LEAST one number")
        else:
            return (True, )


    # Main Func to save all data for user. Can update self.userData anywhere but to save data to db must call this func.

    def saveChanges(self):
        """saveChanges - Saves all the changes made from previous calls to the database. Also updates some text on the main menu
        """

        with open('data\mydata.json', 'r+') as f:
            data = json.load(f)
            for i, _ in enumerate(data):
                if _['UserID'] == self.userData['UserID']:
                    data[i] = self.userData


            # Reset pointer to beginning of file after reading. As well as truncating it incase data inputted is smaller than original.

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()


            # Func to update all labels that have old data. Not very important if it fails, wont break anything just wont have uptodate names and pics.

            try:


                # Try to update username text on main menu

                self.userNameLabel.config(text=f'Welcome, \n {self.userData["username"] }' )


                # Try to update profile pic on main menu

                pic = self.getProfilePic()
                self.profilePic.config(image=pic)
                self.profilePic.image = pic
            

            except Exception as e:
                print(e)


            # Allow the settings button to be pressed again.

            self.profilePic.config(state='normal')

            
    # Main warning function. Used to warn the user of any errors. Only need to supply parent and message

    def warning(self, parent, message, bg='red', fg='#fff', fontsize=8, row=5, sticky='ew', columnspan=2):
        """warning Displays a warning message to the user.

        Args:
            parent (Frame): The parent frame to add the warning message to.
            message (str): The message to display to the user.
            bg (str, optional): The background color. Defaults to 'red'.
            fg (str, optional): The foreground color/Color of the text. Defaults to '#fff'.
            fontsize (int, optional): The size of the text in the warning message. Defaults to 8.
            row (int, optional): What row the message should be displayed on. Helps with positiing . Defaults to 5.
            sticky (str, optional): How the warning should stick to the space its given. Defaults to 'ew'.
        """


        warn = tkinter.Label(parent, text=message, bg=bg, fg=fg,border=5, relief="raised", font=(FONT, fontsize), padx=10, pady=10,)
        warn.grid(row=row, column=0, sticky=sticky, padx=20, columnspan=columnspan)


    # Closing Manager For root

    def on_closing(self):
        """on_closing Controls the closing of the root window. Asks for confirmation and will eventaully control saving of data.
        """


        

        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            f = open('HTP.html', 'w')
            f.write("")
            self.root.destroy()


    # Settings menu: Change profile picture, change username, change password, change balance

    def settings(self):
        """settings The main settings function. Generate the modal window and displays all the widgets.
        """


        pic = self.getProfilePic()

        # Disable settings button so multiple windows can't be opened at once. Idiot proofing.

        self.profilePic.config(state='disabled')


        # Creating the settings Modal

        self.settingsModal = tkinter.Toplevel(self.root)
        self.settingsModal.title("Settings")
        self.settingsModal.geometry('460x340')
        self.settingsModal.resizable(False, False)
        self.settingsModal.configure(background=BACKGROUND_COLOR)
        self.settingsModal.wm_attributes("-topmost", 0)


        # Allows user to change profile picture by selecting a new picture from their local disk. 

        def changePic():


            """changePic Asks the user to pick a new picture from their local disk. Also checks if the file is an image and larger than 100x100
            """


            newPic  = askopenfilename(initialdir="images", title="Select Profile Picture", filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("all files", "*.*")))


            # Get width and height of new pic. if less than 100x100, warn user and return, make them pick a new picture.

            (newPicWIDTH, newPicHEIGHT) = Image.open(newPic).size

            if newPicWIDTH < 100 or newPicHEIGHT < 100:
                self.warning(self.settingsModal, "Profile Picture must be miniuim 100x100")
                self.settingsModal.lift()
                return

            self.userData['ProfilePicture'] = newPic
            self.settingsModal.lift()

            try:
                pic = self.getProfilePic()
                self.PicPreview.config(image=pic)
                self.PicPreview.image = pic 
            except:
                print("Something has gone wrong with updating profile pic on settngs")


        # If user discards changes, warn them and get confirmation.
        
        def discard():
            """discard Controls the discard button. Asks the user if they want to discard changes. If they do, closes the modal. Does not save any data
            """


            if messagebox.askokcancel("Close settings", "Are you sure you want to close settings without saving? Your changes will not be saved"):
                self.settingsModal.destroy()
                self.profilePic.config(state='normal')
            else:
                self.settingsModal.lift()


        # bind discard to the 'X' button on the top right of the window.

        self.settingsModal.protocol("WM_DELETE_WINDOW", lambda: discard())


        # Creating and positioning the 2 sub groups of settings: Cosmetic and Passwords

        cosmeticFrame = tkinter.LabelFrame(self.settingsModal, text="Cosmetic", labelanchor="nw", bg=BACKGROUND_COLOR, fg='#fff')
        cosmeticFrame.grid(row=0, column=0, sticky='news', pady=10, padx=20, columnspan=2)

        cosmeticFrame.grid_columnconfigure(2, weight=1)
        cosmeticFrame.grid_rowconfigure(0, weight=1)




        changePasswordFrame = tkinter.LabelFrame(self.settingsModal, text="Passwords", labelanchor="nw", bg=BACKGROUND_COLOR, fg='#fff')
        changePasswordFrame.grid(row=1, column=0, sticky='news', pady=10, padx=20, columnspan=2)


        # Creating and positioning the Current Username label, entry and placeholder

        currentUsername = tkinter.Label(cosmeticFrame, text='Username: ', bg=BACKGROUND_COLOR, fg='#fff')
        currentUsername.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        currentUsernameEntry = tkinter.Entry(cosmeticFrame, width=20, bg=BACKGROUND_COLOR, fg='#fff')
        currentUsernameEntry.grid(row=0, column=1, sticky='w', padx=10,)

        currentUsernameEntry.delete(0, tkinter.END)
        currentUsernameEntry.insert(0, self.userData['username'])


        # Creating and positioning the button to select new profile picture

        profilePicSelector = tkinter.Button(cosmeticFrame, text="Change Profile Picture", bg=BACKGROUND_COLOR, fg='#fff', command= lambda: changePic())
        profilePicSelector.grid(row=1, column=1, sticky='w', padx=10, pady=10, columnspan=3)

        self.PicPreview = tkinter.Button(cosmeticFrame ,image=pic, )
        self.PicPreview.image = pic
        self.PicPreview.grid(row=0, column=2, columnspan=2, rowspan=2, padx=10, pady=10)



        # Creating and positiiing the confrim and new password labels and entries 

        confirmPassword = tkinter.Label(changePasswordFrame, text='Confirm Password: ', bg=BACKGROUND_COLOR, fg='#fff')
        confirmPassword.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        confirmPasswordEntry = tkinter.Entry(changePasswordFrame, width=20, bg=BACKGROUND_COLOR, fg='#fff')
        confirmPasswordEntry.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        newPassword = tkinter.Label(changePasswordFrame, text='New Password: ', bg=BACKGROUND_COLOR, fg='#fff')
        newPassword.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        newPasswordEntry = tkinter.Entry(changePasswordFrame, width=20, bg=BACKGROUND_COLOR, fg='#fff')
        newPasswordEntry.grid(row=1, column=1, sticky='w', padx=10, pady=10)


        # Creating and positioning the save and discard buttons

        saveChanges = tkinter.Button(self.settingsModal, text="Save Changes", bg=BACKGROUND_COLOR, fg='#fff', command= lambda: updateData())
        saveChanges.grid(row=6, column=0, sticky='news', pady=10, padx=20)

        discardChanges = tkinter.Button(self.settingsModal, text="Discard Changes", bg=BACKGROUND_COLOR, fg='#fff', command= lambda: discard())
        discardChanges.grid(row=6, column=1, sticky='news', pady=10, padx=20)


        # Func to update the data in the userData dictionary, and save it to the userData.json file. aswell as close settings. 

        def updateData():
            """updateData Checks to see if supplied data is valid and can be saved. If not it warns the user
            """


            # Check to make sure new username isnt already an account

            wantedUsername = currentUsernameEntry.get()
            with open("data\mydata.json", 'r') as f:
                    for user in json.load(f):
                        if user['username'] == wantedUsername and user['username'] != self.userData['username']:
                            self.warning(self.settingsModal,"Account with that name already exists")
                            return
            self.userData['username'] = wantedUsername


            # This is only here because i messed up the below if statmnent tree, bodge fix.

            if not confirmPasswordEntry.get() and not newPasswordEntry.get():
                self.saveChanges()
                self.settingsModal.destroy()
                return


            # If the user has entered their old password but not a new one, warn the user to do so - also check for the opposite. in either case return and dont update anything.

            if confirmPasswordEntry.get() and not newPasswordEntry.get():
                self.warning(self.settingsModal, "Please enter a new password")
                return
            elif newPasswordEntry.get() and not confirmPasswordEntry.get():
                self.warning(self.settingsModal, "You must confirm your password before changing it")
                return


            # If the user has entered both their old and new password, check if what they entered is actually their password - if not, warn them and return. If it is validate the password is usable.

            else:
                if confirmPasswordEntry.get() == self.userData['password']:
                    valResult = self.validatePassword(newPasswordEntry.get())
                    if valResult[0]:
                        self.userData['password'] = newPasswordEntry.get()
                    else:
                        self.warning(self.settingsModal, valResult[1])
                        return
                else:
                    self.warning(self.settingsModal, "That is not the right password. If you have forgotten your password, contact the admin", fontsize=7, )
                    return


            # If password passes all checks save the changes and close the settings window.

            self.saveChanges()
            self.settingsModal.destroy()


        # settingsModal row and col config

        self.settingsModal.columnconfigure(0, weight=1)
        self.settingsModal.rowconfigure(3, weight=1)


        # Binding the custom focus event to FocusIn click.

        self.settingsModal.bind("<FocusIn>", lambda event: customFocus())


        # Need to use a in the middle func to get the children of the labelFrames. Not an efficent work around but it hasnt broke yet

        def customFocus():
            for labelFrames in self.settingsModal.winfo_children():
                self.focus(labelFrames)


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

        tkinter.Label(self.root, text="Please log in first, if you do not see a log in box \nplease close the program and reopen it.", bg=BACKGROUND_COLOR, fg='#ffffff', font=(FONT, 24)).grid(row=0, column=0, sticky='nesw')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)


        # Hide the main menu screen and adds custom closing manager.

        self.root.iconify()
        self.logInModal.protocol("WM_DELETE_WINDOW", self.on_closing)


        # Func to find what widget has focus, and set it apart if its a text box.

        


        # Func to check if the user has entered a valid username and password. 
        # TODO: Hash the password. 

        def checkLogin(username, password):
            """checkLogin Checks to see if the supplied username and password are valid. if they are, log them in and display the mainmenu, if not call warning()

            Args:
                username (str): The username the user has entered.
                password (str): The password the user has entered.
            """


            if not username or not password:
                self.warning(self.logInModal, "Please fill in all fields")
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
                            self.warning(self.logInModal, "Username or password is incorrect. Try again")
                

        # Func to create a new user, and add it to the data file, if all fields are valid and not taken.

        def createAccount(username, password, confirmPassword):
            """createAccount Creates a new user, and adds it to the data base, aslong as the supplied credentials are valid. and the account name doesnt already exist.

            Args:
                username (str): The username the user has entered.
                password (str): The password the user has entered.
                confirmPassword (str): The password the user has confirmed. Should be the same as password
            """


            valResult = self.validatePassword(password)
            if not username or not password or not confirmPassword:
                self.warning(self.logInModal,"Please fill in all fields")
            elif password != confirmPassword:
                self.warning(self.logInModal,"Passwords do not match")

            elif not valResult[0]:
                self.warning(self.logInModal, valResult[1])
            else:
                with open("data\mydata.json", 'r') as f:
                    for user in json.load(f):
                        if user['username'] == username:
                            self.warning(self.logInModal,"Account with that name already exists")
                            return
                    with open("data\mydata.json", 'r+') as f:
                        data = json.load(f)
                        print("LOADED")
                        print(f'DATA: {data}')
                        data.append({
                                        "UserID": (int(data[-1]['UserID'])) + 1,
                                        "username": username,
                                        "password": password,
                                        "lvl": 1,
                                        "xp":0,
                                        "balance": 100,
                                        "ProfilePicture": "images/default.jpg"
                                        })
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        print(f'DATA2: {data}')
                        print("DUMPED")
                        # time.sleep(0.1)  # add a delay to make sure the file is written. Seems to not need anymore?

                
                # Forcing the first tip the new user sees to be the first one, about how to access settings

                self.BOOT_TIP = True             
                checkLogin(username, password) 

        
        #Creating all the widgets for the login and registration modal.


        # Username Label and Entry Creation

        userNameLabel = tkinter.Label(self.logInModal, text="Username: ", bg=BACKGROUND_COLOR, fg='#fff')
        userNameEntry = tkinter.Entry(self.logInModal,  bg=BACKGROUND_COLOR, fg='#fff', relief="groove" )
        

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

        
        # Binding the focus event to FocusIn click.

        # self.logInModal.bind_all("<FocusIn>", lambda event: self.focus(self.logInModal))

        for child in self.logInModal.winfo_children():
            if isinstance(child, tkinter.Entry):
                child.bind("<FocusIn>", lambda event: self.focus(self.logInModal))


        # Binding the checkLogin to the enter key being pressed while the password entry is focused. // QOL means the user can just use the keybaord to navigate

        passwordEntry.bind("<Return>", lambda event: checkLogin(userNameEntry.get(), passwordEntry.get()))
        

    def BlackJack(self):
        print("black")

    def Dice(self):
        pass

    def Roulette(self):
        print("Routlette")

    def Slot(self):
        print("slots")











































    # Function to create the main menu.

    def mainMenu(self):


        def flipGame(side):
            index = casinoGames.index(self.GameButton.cget("text"))
            if side == "right":
                self.GameButton.config(text=casinoGames [index + 1 if index < len(casinoGames) - 1 else -len(casinoGames)] )  
            else:
                self.GameButton.config(text=casinoGames [index - 1 if index > 0 else len(casinoGames) - 1] )


        # Call getProfilePic for later

        pic = self.getProfilePic()

        
        # Creation and placement of the sidebar frame.

        self.sideBarFrame = tkinter.Frame(self.root, height=WINDOW_HEIGHT,relief='sunken', borderwidth=1, width=200, background=SECONDARY_BACKGROUND_COLOR)
        self.sideBarFrame.grid(row=0, column=0, sticky='nsw')
        

        # Creation and placement of the main frame

        self.mainMenuFrame = tkinter.Frame(self.root, bg=BACKGROUND_COLOR, )
        self.mainMenuFrame.grid(row=0, column=1, sticky='nesw')


        # Column and Row config for the main screen

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=8)
        self.root.rowconfigure(0, weight=1)

        
        # Column and Row config for the sidebar

        self.sideBarFrame.columnconfigure(0, weight=1)
        self.sideBarFrame.columnconfigure(1, weight=1)
        self.sideBarFrame.columnconfigure(2, weight=1)
        self.sideBarFrame.columnconfigure(3, weight=0)
        self.sideBarFrame.rowconfigure(3, weight=1)


        # Creation and placement of the users name at the top of the sidebar

        self.userNameLabel = tkinter.Label(self.sideBarFrame, text=f'Welcome, \n{self.userData["username"]}',font=(FONT, 12), bg=BACKGROUND_COLOR, fg='#fff')
        self.userNameLabel.grid(row=0, column=0, sticky='new', columnspan=3,pady=20, padx=20)


        # Creation and placement of the profile picture at the top of the sidebar

        self.profilePic = tkinter.Button(self.sideBarFrame ,image=pic, command=lambda: self.settings(), pady=10,)
        self.profilePic.image = pic
        self.profilePic.grid(row=1, column=1, sticky='n',)


        # Creation and placement of the Users current chip counter under profile picture.

        self.chipCounter = tkinter.Label(self.sideBarFrame, text=f'Chips: {self.userData["balance"]}', font=(FONT, 12), background=SECONDARY_BACKGROUND_COLOR)
        self.chipCounter.grid(row=2, column=0, padx=20, columnspan=3, sticky='new', pady=10)

        
        # Creation and placement a tips section. 

        TipsFrame = tkinter.LabelFrame(self.sideBarFrame, text="Tips", labelanchor="nw", bd=4, font=(FONT, 12), background=SECONDARY_BACKGROUND_COLOR)
        TipsFrame.grid(row=3, column=0, columnspan=3, sticky='news', pady=10, padx=20)


        # Fetching a random tip from a json file, easy to add more.

        with open("data\\tips.json", "r") as t:
            tip = json.load(t)
            tip = tip[str(random.randint(0, len(tip) - 1))] if not self.BOOT_TIP else tip["0"]
            
           
        # Creation and placement of the tip label.

        Tip = tkinter.Label(TipsFrame, text=tip, justify='left', wraplength=150, font=(FONT, 12), background=SECONDARY_BACKGROUND_COLOR, padx=5)
        Tip.grid(row=0, column=0, sticky='nws', pady=10,)

        TipsFrame.columnconfigure(0, weight=1)


        self.GameButton = tkinter.Button(self.mainMenuFrame, text=casinoGames[0], font=(FONT, 36), background='gray', justify='center', activebackground='gray', command=lambda: self.launchGame(self.GameButton.cget("text")))
        self.GameButton.grid(row=1, column=1, sticky='nwes', )

        self.mainMenuFrame.columnconfigure(0, weight=0)
        self.mainMenuFrame.columnconfigure(1, weight=5)
        self.mainMenuFrame.columnconfigure(2, weight=0)
        self.mainMenuFrame.rowconfigure(0, weight=1)
        self.mainMenuFrame.rowconfigure(1, weight=5)
        self.mainMenuFrame.rowconfigure(2, weight=2)
        # self.mainMenuFrame.rowconfigure(5, weight=1)


        leftArrow = tkinter.Button(self.mainMenuFrame, text="<", font=(FONT, 36), background=BACKGROUND_COLOR, justify='center', border=0, foreground=FOREGROUND_COLOR, command=lambda: flipGame("left"), activebackground=BACKGROUND_COLOR, activeforeground=FOREGROUND_COLOR)
        leftArrow.grid(row=1, column=0, sticky='nws', padx=(20, 0))

        rightArrow = tkinter.Button(self.mainMenuFrame, text=">", font=(FONT, 36), justify='center', border=0, background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, command=lambda: flipGame("right"), activebackground=BACKGROUND_COLOR, activeforeground=FOREGROUND_COLOR)
        rightArrow.grid(row=1, column=2, sticky='nes', padx=(0,20))


        HowToPlay = tkinter.Button(self.mainMenuFrame, text="How to Play", font=(FONT, 12), background=ACCENT_COLOR, foreground=FOREGROUND_COLOR, command=lambda: self.howToPlay(self.GameButton.cget('text')), activebackground=ACCENT_COLOR, activeforeground=FOREGROUND_COLOR)
        HowToPlay.grid(row=2, column=1, sticky='', )


        levelCanvas = tkinter.Canvas(self.mainMenuFrame, background=BACKGROUND_COLOR, border=0, height=50, highlightthickness=0)
        levelCanvas.grid(row=0, column=1, sticky='n', )




        width=200
        radius=20
        top = 10 #5
        height = 30 # 40
        xoffset = 100

        baseXP = 100



        xpamount = levelCanvas.create_text(xoffset+0.5*width, 5+radius, text='Loading...', font=(FONT, 12),  fill=SECONDARY_BACKGROUND_COLOR)



        if self.userData["lvl"] == MAX_LEVEL:
            amountToLevel = self.userData["xp"]
            levelCanvas.itemconfig(xpamount, text='Max Level')
        else:
            for i in range(0, self.userData["lvl"] + 1):
                amountToLevel = int( math.floor( baseXP * ( i ** 1.5) ) ) # eq from https://answers.unity.com/questions/1510240/level-and-xp-system.html
                levelCanvas.itemconfig(xpamount, text=f'{self.userData["xp"]}/{amountToLevel}xp')




        def getLevelBarPercentage():
            return int( (self.userData["xp"] / amountToLevel ) if amountToLevel > 0 else 1 * width+radius )




        xpBarFill = levelCanvas.create_rectangle(xoffset, top, xoffset+getLevelBarPercentage(), top+height, fill=ACCENT_COLOR, outline=ACCENT_COLOR)


        

        levelCanvas.create_line(xoffset, top, width+xoffset, top, fill=SECONDARY_BACKGROUND_COLOR)
        levelCanvas.create_line(xoffset, height+top, width+xoffset, height+top, fill=SECONDARY_BACKGROUND_COLOR)
        levelCanvas.create_arc((width+xoffset + radius, top+height, width+60+radius, top), start=0, extent=90 ,outline=SECONDARY_BACKGROUND_COLOR,  style='arc')
        levelCanvas.create_arc((width+xoffset + radius, top+height, width+60+radius, top), start=270, extent=90 ,outline=SECONDARY_BACKGROUND_COLOR, style='arc')
        



        levelCanvas.create_circle(xoffset, radius+5, radius, fill=BACKGROUND_COLOR, outline=SECONDARY_BACKGROUND_COLOR)
        playerLevel = levelCanvas.create_text(xoffset, radius+5, text=str(self.userData["lvl"]), font=(FONT, 12), fill=SECONDARY_BACKGROUND_COLOR)

        levelCanvas.tag_raise(xpamount)








        # Quit Button Creation and placement

        QuitButton = tkinter.Button(self.sideBarFrame, text="Quit", command=self.on_closing, )
        QuitButton.grid(row=4, column=0, sticky='sew', padx=10, pady=10, columnspan=3)


        # Stop sidebar from shrinking or expanding to fit the content. Now the sidebar is always 200 SU

        self.sideBarFrame.grid_propagate(False)

        if not self.testConnection():
            HowToPlay.config(state='disabled')
            self.warning(self.mainMenuFrame, "'How to Play' cannot work without a stable internet connection.\nPlease check your connection and relauch the game.", sticky='',columnspan=3, fontsize=16, row=2)


    # Func to start client. Starts auth first.

    def run(self):
        """run open up the auth menu and start the mainloop
        """


        # Bind custome close manager to root window

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        

        # Start auth process and mainloop func.

        self.auth()
        self.root.mainloop()


# Just making test client and running it.
#TODO: Could be turned into multiplayer. would need to move processing to server script.


h = Client()
h.run()



###TODOS###############################################################################################################################################################

# DONE - Completed 
# WOI - Working on it
# CNC - Cannnot complete
# DNTD - Decided not to do
# IMP - Important
# TODO - To do


#TODO: make settings actually look good. Placements are a bit weird atm -- # DONE
#TODO: Allowing for more types of images for pics -- # DONE
#TODO: Limit allowed profile pics to min size. 100x100? -- # DONE
#TODO: Figure out what to put in sidebar white space - Tips? Leaderboard? -- # DONE
#TODO: Look into multiplayer support. - Game is already kinda set up for it. Just need server and porting -- # DNTD
#TODO: Actually make the casino games -- # IMP
#TODO: Make game selection menu - Could do list of buttons or one button that changes. - Look at old casino for how to do that! -- # WOI
#TODO: Proper dev debug menu
#TODO: Xp and Levling system. - wayy further done could unlock.. things? -- # WOI
#TODO: Maybe figure out better way to update db specif items. Very slow atm with lots of seperate instances of opening
#TODO: Look into if python can connect to mongoDB -- # DONE -- will be too much work to transfer over now. Hopefully local json is good enough
#TODO: Make copy of userProfilePic in /images/backup incase pic is deleted from local disk -- # DNTD
#TODO: Sort out all the fonts and sizes - some buttons still clipping -- # DONE
#TODO: Find a suitable theme - do like the dark gray and white atm. Not very casino looking tho.
#TODO: When changing username add the same check as when making a new account. -- # DONE
#TODO: Fix entry focusing issues - Some boxes left highlighted after focus is lost. -- Only on settings screen? -- # DONE
#TODO: Find out how to not let focus run once top level is destroyed. -- # DONE
#TODO: Make it more obvious that settings is accessed by clikcing on profile pic. - Tips Section on first boot? -- # DONE
#TODO: Maybe increase size of main menu. Sidebar is bigger than expected -- # DONE
#TODO: Distinguish quit button from the background. Blends in with the sidebar -- # DONE
#TODO: Fix multiple settings windows being allowed to be open after changing profile pic? Odd behavior. - not sure why this is -- # DONE
#TODO: Find something to fill extra space in settings modal. Or decrease size of modal. -- # DONE
#TODO: Find why username label flickers after clicking back from modal -- #  DONE
#TODO: Find an actaul good looking font for general use. -- # DONE
#TODO: Test if program looks the same on other platforms. - Tkinter uses native components i think
#TODO: Fix focus trying to change the foreground of widgets that dont have a foreground option -- # DONE
#TODO: Add profile pic preview to settings modal -- # DONE
#TODO: Fix changing profile pic so it doesnt update db untill user saves changes. : Allows for user to discard changed profile pic change if they want. -- # DONE
#TODO: Add in fake users -- # DONE
#TODO: Fix bug where setting modal gets hidden behind main screen when chaning profile pic. -- # DONE
#TODO: Move all utils to utils.py 
#TODO: Seperate files for each game? 
#TODO: Add readme in github repo 
#TODO: Sort out comments and docs -- # DONE
#TODO: Add docstrings to all functions : espically utils -- # DONE
#TODO: Add Acount Switching : Sign Out -- # DNTD
#TODO: Find out why creating a new account sometimes fails and messes up the db. -- # DONE // Maybe
#TODO: Fix sidebar changing size -- # DONE
#TODO: Add binding so user can press enter to confirm instead of clicking buttons // QOL -- # DONE
#TODO: Add in a system to get rid off old warning messages. Are starting to clog up the screen and could confuse users. // or stack them up and only show the last one. -- # CNC
#TODO: Add in font settings in the settings modal. Might mess up sizing. // dont allow font size -- # CNC
#TODO: Fix longer tips clipping -- # DONE
#TODO: Look into why cold boot sometimes takes so long 
#TODO: Fix tip not picking last tip in db -- # DONE
#TODO: Find more tips to add to list
#TODO: Look into _tkinter.TclError: invalid command name ".!toplevel2.!labelframe2.!entry" -- # DONE // forgot a return statment
#TODO: Look into password hashing -- # IMP
#TODO: add comments to new game selection section 
#TODO: Look into removing the highlighting when clicking the arrow buttons when switching games -- # DONE
#TODO: add 'How to play' button to main menu -- # DONE
#TODO: Find something to fill white space above gameButton -- # DONE
#TODO: Make/Find full cover images for each game // > 780 x 442
#TODO: plan out how the games will actuall be played. On root screen? or in a modal?
#TODO: Add failsafes in case cover images dont load
#TODO: maybe sub catergorize images to /images/games/<game>/ and /images/users -- # DONE
#TODO: add transition when switching games -- # CNC
#TODO: users level and xp at top of mainscreen instead of in sidebar?? Would fill white space and could use canvas -- # DONE
#TODO: Look into Python-markdown and tkHTML -- # CNC opened md in web broswer instead
#TODO: fill xp bar based on xp % -- # DONE
#TODO: fix clipping issues once xpbar gets near max
#TODO: add max level and change bar to represent that -- # DONE
#TODO: Fix settings modal getting hidden behind other windows if user declines to discard changes -- # DONE
#TODO: Fix spacing on main screen between canvas and game. canvas shouldnt be so big -- # DONE
#TODO: settings modal also gets hidden if seleted profile pic is too small -- # DONE
#TODO: Fix division by 0 error if xp = 0 -- # DONE
#TODO: add how to play functionality -- # DONE
#TODO: finish making the markdown files for all games -- # WOI
#TODO: add check to see if theres network connection if not disable 'how to play button' -- # DONE
#TODO: add LaunchGame function - generalised middle function for launching games -- # DONE
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 
#TODO: 


###MARKS###############################################################################################################################################################

# Input and Output - 1 -- # DONE
# Variables - 1 -- # DONE
# String handling - 1 -- # DONE
# If Statements - 1 -- # DONE

# While Loops - 2 -- IMPOSSIBLE to do with tkinter - MAIN_loop is technically a while # CNC
# For loops - 2 -- # DONE
# Lists - 2 -- # DONE
# Functions - 2 -- # DONE

# 2d Arrays - 3 
# Parameters - 3 -- # DONE
# Return Statments - 3 -- # DONE
# Writing to Files/DataBase - 3 -- # DONE

# GUI - 5 --# DONE

#24/29 = 82%