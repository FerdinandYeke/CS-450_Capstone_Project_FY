# author: Ferdinand Yeke
# date: 1/29/2026 - 3/13/2026
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
    #root = tk.Tk()
    def setWindow():
        root = tk.Tk()
        # This sets the window's size.
        root.geometry("640x320")
        # Sets the title of the window.
        root.title("CaptuR-A-Bot")

        #self.label = tk.Label(self.root, text="")
        label = tk.Label(root,text="Welcome to the Web Bot Detection Application.\n" \
        "This application takes in a Website URL of a Social Media site or a E-Commerce site and sees if there" \
        " are any nerfarious bots in a site.\n" \
        "It does this by the use of Agentic LLMs that researches the site itself, reports what is on the site, " \
        "and tries to see contextes and patterns of a site's that shows any signs of bad bots.")
        label.pack()
    # Text Widget box gets added first here.
        text_widget = tk.Text(root, height= 30, width= 100)
    # Inserts Predefined text into the box.
        # This is just a test for read-only text window. This will have ongoing text from
        #   the agents with the 'agents_output' parameter in the setWindow function, where
        #   text from the agents will be outputted there.
        text_widget.insert(tk.END, "This is a test.")
    # Prevents edits into the text box, since it edits by default.    
        text_widget.config(state= tk.DISABLED)
        #self.responses = responses
    # Packs the Text Widget Box for responses.
        text_widget.pack(padx= 10, pady= 10)

    # Text Widget Section ends here. Might put it all in another method later.

    #root.mainloop() #root.mainloop might be a boolean once all parameters in the methods have 
    # been used, while also might being at the end of this class.

    # Text section for pasting website URL in the window starts here.
        user_text_widget = tk.Text(root, height= 5, width= 100)
        user_text_widget.pack(padx=3, pady=3)

        root.mainloop()
    response = "This is a test."
    setter = setWindow()
    setter

    def newButtons():
        pass       
    # getThatEntry = setEntry()
    # getThatEntry
    
    # Function of generating a new frame for the GUI
    def newFrame():
        pass


