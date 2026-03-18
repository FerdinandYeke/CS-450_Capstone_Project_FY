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
# Imports necessary classes and sets up essential objects.
import tkinter as tk
import queue
#root = tk.Tk()
#text_widget = tk.Text(root, height= 30, width= 100)
#user_text_widget = tk.Text(root, height= 5, width= 100)

#text_insert: str
class WebBotWindow:
    # setWindow sets the window. (This is also newLabels())
    #def setWindow(text_insert) -> str:

    # Default Constructor of the WebBotWindow Class with Setting up the main GUI Window.
    # This default constructor used to have a text_insert parameter, but is now unnecessary.
    def __init__(self, start_flow_callback):
        """"Contructs the Main Window GUI, containing the Text Output Field, and the User Input Field."""
         # For staying on sync with the agents and terminal, the queue class is used.
        self.msg_Queue= queue.Queue() # For staying on sync with the agents and terminal, the queue class is used.
        self.start_flow_callback = start_flow_callback # Stays on track with the main.py Flows.

        #self.text_insert = text_insert
        # 1. The root is called.
        self.root = tk.Tk() # Recalls the root variable above.
        self.root.geometry("640x500") # 2. Sets up the basic window.
        self.root.title("CaptuR-A-Bot") # 3. Names the title of the window.
        # 4. Makes a label on top of the window.
        self.label = tk.Label(self.root,text="Welcome to the Web Bot Detection Application.\n" \
        "This application takes in a Website URL of a Social Media site or a E-Commerce site and sees if there" \
        " are any nerfarious bots in a site.\n" \
        "It does this by the use of Agentic LLMs that researches the site itself, reports what is on the site, " \
        "and tries to see contextes and patterns of a site's that shows any signs of bad bots.")
        self.label.pack() # Packs it.
        # 5. Calls the construct widget class in to construct all the entry fields, buttons and the message box.
         # Sets up the text output where a user and agent's responses appear in.

        # 3/18/2026 from the first label line here to the last entry line in this constructor, this was from the construct widgets.
        #   The code is now here to prevent double windows from occuring due to calling the construct_widgets() that contain all of this
        #   Construct widgets start here

        self.text_output_Box = tk.Text(self.root, height=32, width=128)
        #self.text_output.config(state=tk.DISABLED) # Make it read-only
        self.text_output_Box.see(tk.END) # Automatically scrolls to the bottom of the text box.
        self.text_output_Box.config(state=tk.DISABLED) # After the new text, it immediately makes the text read-only.
        self.text_output_Box.pack()
        #self.message_Box(text_insert) # --Prints out the given text inserted and outputs it into the text box.
        # Text Output Field setup ends here.


        # Rather than setting a text field, this sets up a simple
        #   One-lined field instead.

        # --Sets up the label for Website URL.

        self.web_url_Label = tk.Label(self.root, text="Enter URL: ")
        self.web_url_Label.pack()
        # --Label for Website URL ends here.
        # --Sets up the Website URL Entry Field.

        self.url_entry_widget = tk.Entry(self.root, width=50)
        self.url_entry_widget.pack()
        # --Website URL Entry Field ends here.

        # --Sets up the label field for website type.

        self.web_type_label = tk.Label(self.root, text="Website Type (social_media or e-commerce):")
        self.web_type_label.pack()
        # --Web type label ends here.
        # --Sets up the Website Type entry field for website type.

        self.web_type_entry = tk.Entry(self.root, width=20)
        self.web_type_entry.pack(pady=5)
        # --Web type entry field ends here.

        # Sets up the Label for Bot Type. 

        self.bot_type_label = tk.Label(self.root, text="Bot Type (good_bots or bad_bots):")
        self.bot_type_label.pack()
        # Bot Type Label ends here.
        # Sets up the entry for the bot type.

        self.bot_type_entry = tk.Entry(self.root, width=20)
        self.bot_type_entry.pack(pady=5)
        # Bot Type Entry ends here.

        # Sets up the submit button for the user after all entrys are inputted by the user.

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_input)
        self.submit_button.pack(pady=10)
        # Submit Button field setup ends here.
        # Construct Widgets ends here.

        self.refreshWindow() # 6. After the construct_widgets() method is called, it then refreshes the message window for new messages.
    # __init__ method ends here.

    # This method could be used later for resizing the window.
    def setWindow(self):
        pass
    #root.mainloop()


# Returns the entry's values to the agents in str format.
    # Returns the URL.
    def return_URL_entry(self):
        """Returns the URL to the Agents."""
        return self.url_entry_widget.get()
    # Return URL method ends here.

    # Returns the Bot Type
    def return_bot_type_entry(self):
        """Returns the Bot Type to the Agents."""
        return self.bot_type_entry.get()
    # Return Bot Type entry method ends here.
    
    # Reeturns the Web Type.
    def return_web_type_entry(self):
        """Returns the Web Type to the Agents."""
        return self.web_type_entry.get()
    #Return Web Type Entry Method ends here.
    

    # * VERY IMPORTANT!!! This is a foundational method that puts everything that the GUI needs, like the Message Text Box, Entry fields, all into a 
    #   nice, compact method for the main initialization method!

    #def construct_widgets(self): # Used to be a text_insert object, but is unecessary.
        # 3/18/2026: Code now moved to the __init__ method to prevent double windows.
    #    pass

    # Submit_input function starts here. This method gets all of the entries from the fields, submits it and prints out the message
    #   of the agents reviewing the given URL. (with accounting for the web type and bot type, of course.)
    def submit_input(self):
        """Retrieves all the inputted values in the entry fields, while making a key/value pair of it."""
        website_URL = self.url_entry_widget.get() # Gets the website URL via entry.
        web_type = self.web_type_entry.get() # Gets the website type via entry.
        bot_type = self.bot_type_entry.get() # Gets the bot type via entry.

        # 1. Makes a key/value pair of the above values for complete entry scope.
        data = {
            "website_url" : website_URL,
            "website_type" :  web_type,
            "bot_type" : bot_type
        }
        # 2. This just prints out the website URL that the agents are currently looking at.
        self.message_Stream(f"System: Agents are now currently looking at {data['website_url']}!")

        #print(f"URL: {website_URL}, Type: {web_type}, Bot: {bot_type}") #print to console for testing.
        #self.text_output.config(state=tk.NORMAL) # Enable writing to the text widget
        #self.text_output.delete("1.0", tk.END) # Clear the widget
        #self.text_output.insert(tk.END, f"You entered:\nURL: {website_URL}\nType: {web_type}\nBot: {bot_type}\n")
        #self.text_output.config(state=tk.DISABLED)  # Disable again

        # 2. Next, The Flow will reference this.
        #self.start_flow_callback(data,self.msg_Queue)

    # Submit input function ends here.

    # Message Stream method starts here.
    # This is not the same as the Text Output Box, but they are connected! This method 
    #       * takes in a message from an agent or user,
    #       * passes that into the message parameter, 
    #       * reuses the text_output_Box Text instance, 
    #       * inserts the message into the text box.
    def message_Stream(self, message):
        """Outputs a text from an Agent or User, and prints that onto the Text Output Field."""
        self.message = message
        # New code starts here (3/17/2026).
        #self.text_output.config(state=tk.DISABLED) # Does not let the user input text
        #self.text_output.delete("1.0", tk.END) # Deletes the oldest messages in the text. Will be removed later.
        #self.text_output.insert(tk.END, text_output)
        #self.text_output.config(state=tk.DISABLED)

        self.text_output_Box.config(state=tk.NORMAL)
        self.text_output_Box.insert(tk.END, f"\n> {message}\n") # Gets the text output, formats it, and goes to the next line.
        self.text_output_Box.see(tk.END) # Automatically scrolls to the bottom of the text box.
        self.text_output_Box.config(state=tk.DISABLED) # After the new text, it immediately makes the text read-only.

    #def run_main_loop(self):
    #    root.mainloop()
    
    # Check queue method starts here.
    def refreshWindow(self):
        """This checks the queues from messages by the agents every 100ms. (This just refreshes the textbox.)"""
        try:
            while(True):
                new_message = self.msg_Queue.get_nowait()
                self.message_Stream(new_message)
        except queue.Empty:
            pass
        self.root.after(100, self.refreshWindow)
    # Check queue method ends here.

    # run_main_loop method starts here
    def run_main_loop(self):
        """After setting up the basic window, this function runs the window with the Tkinter mainloop() function."""
        self.root.mainloop()
    
    # Text Output ends here.

    # OK. SO, I am planning to have the lines of code that lets the user input entry stuff with their own method, and they will
    #   instead RETURN VALUES to the terminal. (3/17/2026) Work in progress (5:48 pm)
#runit = WebBotWindow()
#runit.construct_widgets()
#runit.run_main_loop()