# imports

import tkinter
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from pathlib import Path
import time
from tkinter.filedialog import askopenfilename


# Constants

casinoGames = ["Blackjack", "Poker", "Dice"]
WINDOOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = "#1d1d1d"
DEBUG = False


# Initalize the client class ### Maybe allowing for multiplayer? only lan with ports?

class Client:
    def __init__(self):


        # Initialize the root window

        self.root = tkinter.Tk()
        self.root.title("Casino")
        self.root.geometry(f'{WINDOOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.root.configure(background=BACKGROUND_COLOR)


    # Function to get the users profile pic. If the original file is not found, it will return the default profile pic.

    def getProfilePic(self):
        try:
            profilePic = Image.open(self.userData['ProfilePicture'])
        except:
            print("Something went wrong when trying to get the profile picture. Restorted back to default")
            profilePic = Image.open("images/default.jpg")

        pic = profilePic.resize((75,75), Image.ANTIALIAS)
        pic = ImageTk.PhotoImage(pic)
        return pic


    # Function to validate wether the users password is acceptable. Used in create account and change password.

    def validatePassword(self, password):
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


                # Try to cupdate profile pic on main menu

                pic = self.getProfilePic()
                self.profilePic.config(image=pic)
                self.profilePic.image = pic
            

            except Exception as e:
                print(e)


            # Allow the settings button to be pressed again.

            self.profilePic.config(state='normal')

            
    # Main warning function. Used to warn the user of any errors. Only need to supply parent and message

    def warning(self, parent, message, bg='red', fg='#fff', fontsize=8, row=5, sticky='ew'):
            warn = tkinter.Label(parent, text=message, bg=bg, fg=fg,border=5, relief="raised", font=('Helvetica', fontsize), padx=10, pady=10)
            warn.grid(row=row, column=0, sticky=sticky, padx=20, columnspan=2)


    # Closing Manager For root

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


    # Settings menu: Change profile picture, change username, change password, change balance

    def settings(self):


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
            newPic  = askopenfilename(initialdir="images", title="Select Profile Picture", filetypes=(("png files", "*.png"), ("all files", "*.*")))
            self.userData['ProfilePicture'] = newPic
            self.saveChanges()


        # If user discards changes, warn them and get confirmation.
        
        def discard():
            if messagebox.askokcancel("Close settings", "Are you sure you want to close settings without saving? Your changes will not be saved"):
                self.settingsModal.destroy()
                self.profilePic.config(state='normal')


        # bind discard to the 'X' button on the top right of the window.

        self.settingsModal.protocol("WM_DELETE_WINDOW", lambda: discard())


        # Func to find what widget has focus, and set it apart if its a text box.

        def focus(event):
            widget = self.settingsModal.focus_get()
            widget.configure(relief="solid", borderwidth=2, bg='#fff', fg='#000')
            for child in self.settingsModal.winfo_children():
                if child != widget and child.winfo_class() == "Entry":
                    child.configure(relief="groove", borderwidth=1, bg=BACKGROUND_COLOR, fg='#fff')


        # Creating and positioning the 2 sub groups of settings: Cosmetic and Passwords

        cosmeticFrame = tkinter.LabelFrame(self.settingsModal, text="Cosmetic", labelanchor="nw", bg=BACKGROUND_COLOR, fg='#fff')
        cosmeticFrame.grid(row=0, column=0, sticky='news', pady=10, padx=20, columnspan=2)

        changePasswordFrame = tkinter.LabelFrame(self.settingsModal, text="Passwords", labelanchor="nw", bg=BACKGROUND_COLOR, fg='#fff')
        changePasswordFrame.grid(row=1, column=0, sticky='news', pady=10, padx=20, columnspan=2)


        # Creating and positioning the Current Username label, entry and placeholder

        currentUsername = tkinter.Label(cosmeticFrame, text='Username: ', bg=BACKGROUND_COLOR, fg='#fff')
        currentUsername.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        currentUsernameEntry = tkinter.Entry(cosmeticFrame, width=20, bg=BACKGROUND_COLOR, fg='#fff')
        currentUsernameEntry.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        currentUsernameEntry.delete(0, tkinter.END)
        currentUsernameEntry.insert(0, self.userData['username'])


        # Creating and positioning the button to select new profile picture

        profilePicSelector = tkinter.Button(cosmeticFrame, text="Change Profile Picture", bg=BACKGROUND_COLOR, fg='#fff', command= lambda: changePic())
        profilePicSelector.grid(row=1, column=0, sticky='w', padx=10, pady=10)


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
            self.userData['username'] = currentUsernameEntry.get()


            # This is only here because i messed up the below if statmnent tree, bodge fix.

            if not confirmPasswordEntry.get() and not newPasswordEntry.get():
                self.saveChanges()
                self.settingsModal.destroy()


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


        # Binding the focus event to mouse click.

        self.settingsModal.bind_all("<Button-1>", lambda event: focus(event))


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


        # Call getProfilePic for later

        pic = self.getProfilePic()

        
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
        self.sideBarFrame.rowconfigure(3, weight=1)


        # Creation and placement of the users name at the top of the sidebar

        self.userNameLabel = tkinter.Label(self.sideBarFrame, text=f'Welcome, \n{self.userData["username"]}',font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg='#fff')
        self.userNameLabel.grid(row=0, column=0, sticky='new', columnspan=3,pady=20, padx=20)


        # Creation and placement of the profile picture at the top of the sidebar

        self.profilePic = tkinter.Button(self.sideBarFrame ,image=pic, command=lambda: self.settings(), pady=10,)
        self.profilePic.image = pic
        self.profilePic.grid(row=1, column=1, sticky='n',)


        # Creation and placement of the Users current chip counter under profile picture.

        self.chipCounter = tkinter.Label(self.sideBarFrame, text=f'Chips: {self.userData["balance"]}', font=("Helvetica", 12))
        self.chipCounter.grid(row=2, column=0, padx=20, columnspan=3, sticky='new', pady=10)

        
        # Creation and placement a tips section. 
        # TODO: Might change later. leaderboard? Recent games? not sure. just didnt like all the white space.

        TipsFrame = tkinter.LabelFrame(self.sideBarFrame, text="Tips", labelanchor="nw", bd=4, font=("Helvetica", 12))
        TipsFrame.grid(row=3, column=0, columnspan=3, sticky='news', pady=10, padx=20)

        
        # Quit Button Creation and placement

        QuitButton = tkinter.Button(self.sideBarFrame, text="Quit", command=self.on_closing, )
        QuitButton.grid(row=4, column=0, sticky='sew', padx=10, pady=10, columnspan=3)


        # Debug option so i know what profile im working with. 
        #FIXME : Remove this later.

        self.root.bind('<Return>', lambda event: print(self.userData))


    # Func to start client. Starts auth first.

    def run(self):


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

#TODO: make settings actually look good. Placements are a bit weird atm
#TODO: Allowing for more types of images for pics
#TODO: Limit allowed profile pics to min size. 100x100?
#TODO: Figure out what to put in sidebar white space - Tips? Leaderboard?
#TODO: Look into multiplayer support. - Game is already kinda set up for it. Just need server and porting
#TODO: Actually make the casino games
#TODO: Make game selection menu - Could do list of buttons or one button that changes. - Look at old casino for how to do that!
#TODO: Proper dev debug menu
#TODO: Xp and Levling system. - wayy further done could unlock.. things?
#TODO: Maybe figure out better way to update db specif items. Very slow atm with lots of seperate instances of opening
#TODO: Look into if python can connect to mongoDB
#TODO: Make copy of userProfilePic in /images/ incase pic is deleted from local disk
#TODO: Sort out all the fonts and sizes - some buttons still clipping
#TODO: Find a suitable theme - do like the dark gray and white atm. Not very casino looking tho.
#TODO: When changing username add the same check as when making a new account.
#TODO: Fix entry focusing issues - Some boxes left highlighted after focus is lost.
#TODO: Make it more obvious that settings is accessed by clikcing on profile pic. - Tips Section on first boot?
#TODO: Maybe increase size of main menu. Sidebar is bigger than expected
#TODO: Distinguish quit button from the background. Blends in with the sidebar
#TODO: Fix multiple settings windows being allowed to be open after changing profile pic? Odd behavior. - not sure why this is
#TODO: Find something to fill extra space in settings modal. Or decrease size of modal.
#TODO: Find why username label flickers after clicking back from modal
#TODO: Find an actaul good looking font for general
#TODO: Test if program looks the same on other platforms. - Tkinter uses native components i think
#TODO: Fix focus trying to change the foreground of widgets that dont have a foreground option
#TODO: 
