#!/usr/bin/env python
from datetime import date
import json
import os
import sys
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from crewai.agent import Agent
from datetime import datetime
# Imports the BotDetectionOrche class (short for Orchestration) in this main file.
from bot_flow.crews.bot_detection_orche.bot_detection_orche import BotDetectionOrche
from bot_flow.WebBot_GUI import WebBotWindow  # Adjust the path if needed

# Imports the web_Bot GUI class

import tkinter as tk
from typing import Optional
import threading
from queue import Queue
# 3/4/2026: The web bot window class will be planned to be imported into this class.

# Firstly, the flow state will be defined with related objects.
#lock = threading.Lock() # global variable.
#main_gui = WebBotWindow()
class Guide_Web_Bot_State(BaseModel):
    web_type: str = ""
    topic: str = ""
    bot_detect_type: str = ""
    website_URL: str = ""
    results: str = ""
    #results: Optional[str] = None
    current_year: datetime = ""
    current_date: datetime = ""
    # current_year: date.year 
class Guide_Web_Bot_Flow(Flow[Guide_Web_Bot_State]):
    """This is a flow for making a bot detection on a website."""
    # --Calls the super class from WebBotWindow
    # --This first initializes the agents state as None for the thread.
    def __init__(self, state: Optional[Guide_Web_Bot_State] = None, gui: Optional[WebBotWindow] = None):
        super().__init__(state or Guide_Web_Bot_State())
        #self.main_gui = gui
        self.gui = gui

    # Super class call & function ends here.
    @start()
    # Get User Input GUI method/function starts here.
    def get_user_input_GUI(self):
        """This gets input from the user, where this input is a URL that checks to see bots in the website.
        * Instead of getting inputs by terminal like the main_OLD.py file, this does it via GUI."""

        #self.main_gui = main_gui
        # User is first greated while awaiting inputs.
        #self.main_gui.message_Stream("Greetings from Web Bots!\n This tool will help you check on a website's bot traffic." \
        #"\nThis Tool can also let you check good bots, nefarious bots, or both on a site while " \
        #"giving you info on them! \nEnter the URL, Website Type, and Bot_type to Start!")

        
        # Retrives the url from the GUI first before the input_Operation.
        #self.state.website_URL = (self.state.website_URL or "").strip()
        url = self.state.website_URL.strip()
        b_type = self.state.bot_detect_type.strip()
        w_type = self.state.web_type.strip()
        if not url and not b_type and not w_type:
            #self.state.results = "Empty URL field."
            self.state.results = "One or more fields are empty."
            return ""
        return url
    

    # After the get_user_input_GUI returns at least one value (url), it
    #   the input_Operation starts execution of crew kickoff,
    @listen(get_user_input_GUI)
    def input_Operation(self, url: str):
        # This uses the gui.msg_Queue method due to its nature being thread safe.
        #   This will put messages into the gui box instead of message_Stream for thread safety.
        """Agents run off of the user's input."""

        try:
            self.state.results = "Starting agent orchestration..."

            # 4/16/2026 (message box Fix): msg_Queue (or Queue) is one of the most important objects for this flow.
            #   With this, it can pass messages from the background process (agents) to the gui. By putting the message
            #   in a queue, and the getting it and formatting it to the GUI, messages from the background
            #   process are passed SAFELY to the GUI!
            self.gui.msg_Queue.put("Agents Launched!\nAgents now analyzing website....\nPlease wait for final results....") # This will be the first message to print out.
            self.gui.msg_Queue.put("Gathering inputs for the Agents....") # This will be the second message to print.
           
            # 4/16/2026 (Quick Fix): Instead of just relying on states, I will instead just fetch the inputs as soon as pressing the submit button.
            self.state.website_URL = self.gui.return_URL_entry()
            self.state.web_type = self.gui.return_web_type_entry()
            self.state.bot_detect_type = self.gui.return_bot_type_entry()

            # Gathers the inputs from the GUI and the states, while mapping them as key/value pairs.
            inputs = {
                "current_year": str(datetime.now().year), 
                "website_URL": self.state.website_URL, 
                "web_type": self.state.web_type, 
                "bot_detect_type":self.state.bot_detect_type,
                "topic":"web bots",
                "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"
            }

            self.gui.message_Stream(self.gui.msg_Queue.get_nowait())
            self.gui.message_Stream(self.gui.msg_Queue.get_nowait())

            crew = BotDetectionOrche().crew() # --Calls the BotDectOrche Class and the crew() function.

            agents_Assemble = crew.kickoff(inputs=inputs) # --The .kickoff starts, with the inputs above being stored in the inputs parameters here.

            raw = getattr(agents_Assemble, "raw", None) # --This is the same as --> self.state.results = agents_Assemble.raw
            #self.state.results = agents_Assemble.raw
            self.state.results = f"Agent results: {raw if raw is not None else str(agents_Assemble)}"

            # --Once the agents are done, the formatted results gets stored in the msg_Queue Queue, which will then get printed out in the message Stream.
            self.gui.msg_Queue.put(f"Agents website analysis complete!\nHere's what we got: {self.state.results}")
            self.gui.message_Stream(self.gui.msg_Queue.get_nowait()) # --Gets the results and prints it out to the message box!
        # --Otherwise, if crew kickoff does not work, then the application will print of a "Agent Execution Failure" message in the message box.
        except Exception as e:
            self.state.results = f"Agent execution failed: {e}" 
            self.gui.msg_Queue.put(f"🚨 FAILURE: Agent execution failed. Details{e}")
            self.gui.message_Stream(self.gui.msg_Queue.get_nowait())
        return self.state.results
    # --Input Operation GUI ends here.

#----------------
# AppController Class starts here
#----------------
# --This is a class that contains the new instance of WebBotWindow. It manages the instance while safely launching the thread for agent execution
#   via "Submit" Button.
class AppController:
    # ------------------ Initialized App function starts here.
    def __init__(self, root: tk.Tk):
        """Manages the app while using a thread targeting agent flow."""
        self.root = root
        # --This reuses the superclass WebBotWindow from the WebBotGUI.py file.
        self.gui = WebBotWindow()

        # --Submit button: This here BINDS the submit button to a wrapper, which
        #   makes the Submit button actually start the flow.
        try:
            # --While the Submit Button is on the GUI, assume that it works and commands the agents once clicked.
            # --The message_Stream message here is the FIRST MESSAGE TO PRINT UPON LAUNCH!!!
            self.gui.message_Stream("Greetings from Web Bots!\n This tool will help you check on a website's bot traffic." \
            "\nThis Tool can also let you check good bots, nefarious bots, or both on a site while " \
            "giving you info on them! \nEnter the URL, Website Type, and Bot_type to Start!")
            self.gui.submit_button.config(command=self.during_submit) # The Submit Button's command is the during_submit() function.
        except Exception:
            # Otherwise, the override button command from WebBotWindow is used to call the agents thread.
            #if hasattr(self.gui, "override_button_command"):
            #    self.gui.override_button_command(return_agents_Thread=self.during_submit) # works like the submit_button.config() function.
            pass
        self.agents_worker_thread = None
    # --------------- Initialized App function ends here.

    # --------------- collection_state_gui() function starts here.
    def collection_state_GUI(self) -> Optional[Guide_Web_Bot_State]:
        """Acts as the extension of the get_user_input method, where it retrives entries
        and has the submit button to rely with."""
        
        # Fetches the entries from the gui by using the gui class attributes. (Upon testing, they are actually null and is replaced by the input_Operation() function.)
        url_entry = self.gui.return_URL_entry()
        web_type_entry = self.gui.return_web_type_entry()
        bot_type_entry = self.gui.return_bot_type_entry()
        
        # Returns the NEW Guide_Web_Bot_State with newly set variables for the parameters of
        #   the inital instance of Guide_Web_Bot_State.
        return Guide_Web_Bot_State(website_URL= url_entry, web_type= web_type_entry,
                                    bot_detect_type= bot_type_entry)
    # -----------------collection_state_gui() function ends here.

    # ----------------During_Submit() funtion starts here.
    def during_submit(self):
        """Serves as the command for the Submit Button. This function does the following (in order):
            * Gets the states from Guide_Web_Bot_State.
            * Prints out that the Flow has started once Submit button is clicked.
            * Locks the Submit Button.
            * Creates a thread (specifically a background one) that targets the 
                _agent_flow_worker function (**which kickoffs the entire Guide_Web_Bot_Flow class, and prints out messages from the agents**)."""
        # --Uses the input states from the GUI.
        state = self.collection_state_GUI()

        # --GUI responds to the input.
        try:
            self.gui.message_Stream("Okay, Agents Assemble!") # --As soon as the user clicks the submit button, if succesful, this message prints out here. (no need for a queue for messages.)
            self.gui.lock_Submit_Input() # --Locks the submit input button upon succesful inputs.
        except Exception:
            pass
        # --Now, a thread for the agents is made here.
        self.agents_worker_thread = threading.Thread(target= self._agent_flow_worker, 
                                              args= (state,), daemon = True)
        # --The reason args is set to state is because of flows nature on relying on states to proceed through
        #   steps in code bodies to the end.
        self.agents_worker_thread.start() # --Starts the thread (which runs in the background of the gui!).
    # ----------------During_Submit() function ends here.

    # ---------------- agent_flow_worker() function starts here
    def _agent_flow_worker(self, state: Guide_Web_Bot_State): # Utilizes the newly retrieve inputs from the GUI while being states.
        #"""Acts as a worker for the Flow, where it runs the Flow while also updating the GUI."""
        """ This function gets targeted by the agents_worker_thread, instansiates the flow class Guide_Web_Bot_Flow, and kicks off the flow class."""

        # --flow is a new Guide_Web_Bot_Flow instance for kicking off the Flow.
        # --state=state means that the new state is equal to the entries retrived and set in Guide_Web_Bot_State.

        flow = Guide_Web_Bot_Flow(state=state, gui=self.gui) # --Packs the entire Web_Bot_Flow Class and uses the new states and the same self.gui object.
        # --This here runs the flow synchronously (which blocks only the agents_worker_thread).
        
        # try/catch block starts here
        try:
            flow.kickoff() # --Kicks off the entire flow class!

            self.gui.msg_Queue.put(f"{flow.state}") # --Puts the flow.state values onto the msg_Queue, and prints out states of the agents.
            self.gui.root.after(50, lambda: self.gui.refreshWindow(self.gui.msg_Queue.get_nowait())) # --Calls the get no_wait function and uses the refresh window to check any new messages.
        except Exception as e:
            flow.state.results = f"Flow operation failed. {e}" # --If flow failed to kickoff, the message will be printed into the message box.

        # --Stores the results of the flow into variable final_text.
        final_text = flow.state.results or "No results."
        self.gui.msg_Queue.put(f"{final_text}") # --Safely PUTS the final text (formatted) in the msg_Queue.
        format_Final = self.gui.msg_Queue.get_nowait() # --Safely GETS the final text (since it is the first in line here) from the queue and it gets printed to the window.
        self.gui.root.after(100, lambda: self.gui.refreshWindow(format_Final)) # --Puts the final message in the message box.
        
    # ------------------- agent_flow_worker ends here.    


# Runs the Guide Web Bot Flow class.
def kickoff():
    """ Overwritten kickoff function for kicking off the app and flow."""
    root = tk.Tk() # Instantiates a new tk instantance.
    root.withdraw() # Prevents a duplicate window.
    app = AppController(root) # Uses the root variable for the AppController's functions, while also being a new instance of AppController.

    # Since the app has the run_main_loop function, it will use that command to start the gui, other wise, use the root.main_loop().
    try:
        if hasattr(app.gui, "run_main_loop"):
            app.gui.run_main_loop()
            return
        # Planning to add a feature to where if a user exits the program, the flow cancels.
        #if(root.destroy() is True):
            
    except Exception:
        pass
    root.mainloop()

    #bot_flow.kickoff()

# Plots the Guide Web Bot Flow class.
def plot():
    pass
#     bot_flow = Guide_Web_Bot_Flow()
#     bot_flow.plot("WebBotFlowPlot")
   
# Executes both the kickoff and plot functions.
if __name__ == "__main__":
    kickoff()
    #main_gui = WebBotWindow
    #app = main_gui.run_main_loop()
    # 3/3/2026: Plot will be done later.
#    plot()
    # Finally, once the kickoff starts, the gui does as well.
# Class ends here.