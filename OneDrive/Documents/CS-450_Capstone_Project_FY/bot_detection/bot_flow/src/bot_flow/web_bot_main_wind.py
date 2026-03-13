# author: Ferdinand Yeke
# date: 1/29/2026
# Class description:
#   This is a class that will have a Graphical User Interface that lets users input a website,
#   such as a of a e-commerce site like Amazon.com or a social media site like Facebook, while
#   letting Agentic LLMs seeing if there are any nefarious bots in a specific post.
#   
#   Once it runs through the specific post/site, it will then print out details of the bad bots like
#   account name and history, while doing a well documented report of them to report to website admins to
#   review.
# 
#   Widgets that will be used:
#       Labels
#       Buttons
#       Entry
#       Frame
#  
#from bot_detection.bot_flow import main

import tkinter as tk
class webBotWindow():
    # setWindow sets the window. (This is also newLabels())
    root = tk.Tk()
    def setWindow(self):
        self.root = tk.Tk()
        # This sets the window's size.
        self.root.geometry("640x320")
        # Sets the title of the window.
        self.root.title("CaptuR-A-Bot")

        #self.label = tk.Label(self.root, text="")
        self.label = tk.textbox(self.root,text="Welcome to the Web Bot Detection Application.\n" \
        "This application takes in a Website URL of a Social Media site or a E-Commerce site and sees if there" \
        " are any nerfarious bots in a site.\n" \
        "It does this by the use of Agentic LLMs that researches the site itself, reports what is on the site, " \
        "and tries to see contextes and patterns of a site's that shows any signs of bad bots.")
        self.label.pack()
       #root.mainloop() #root.mainloop might be a boolean once all parameters in the methods have been used, while also might being at the end of this class.
    # Entry method for pasting website URL in the window.
    def setEntry(self, url_input):
        root = tk.Tk()
        entry = tk.Entry(root)
        tk.Entry(root, text="Enter URL:").pack(pady=10)
        self.url_input = entry.get()
        root.mainloop()
    setter = setWindow()
    setter

    def newButtons():
        pass       
    # getThatEntry = setEntry()
    # getThatEntry
    
    # Function of generating a new frame for the GUI
    def newFrame():
        pass


