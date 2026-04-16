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
    # Calls the super class from WebBotWindow
    #def __init__(self, gui=WebBotWindow()): # This first initializes the agents state as None for the thread.
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
    def input_Operation(self, website_URL: str):
        # This uses the gui.msg_Queue method due to its nature being thread safe.
        #   This will put messages into the gui box instead of message_Stream for thread safety.
        """Agents run off of the user's input."""
        # 🚨 CRITICAL FIX: Do NOT rely on the input variable `website_URL` 
        # for *all* the data. Read everything needed from the self.state object 
        # which was populated by AppController.

        try:
            self.state.results = "Starting agent orchestration..."

            #self.main_gui.message_Stream("Agents now currently analyzing the website...")
            #agents_Assemble = BotDetectionOrche().crew().kickoff(inputs={"current_year": str(datetime.now().year), "website_URL": self.state.website_URL, 
            #                                                "web_type": self.state.web_type, 
            #                                                "bot_detect_type":self.state.bot_detect_type,
            #                                                "topic":"web bots",
            #                                                "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"})

            # 4/16/2026 (message box Fix): msg_Queue (or Queue) is one of the most important objects for this flow.
            #   With this, it can pass messages from the background process (agents) to the gui. By putting the message
            #   in a queue, and the getting it and formatting it to the GUI, messages from the background
            #   process are passed SAFELY to the GUI!
            self.gui.msg_Queue.put("Gathering inputs for the Agents....")
           
            # 4/16/2026 (Quick Fix): Instead of just relying on states, I will instead just fetch the inputs as soon as pressing the submit button.
            self.state.website_URL = self.gui.return_URL_entry()
            self.state.web_type = self.gui.return_web_type_entry()
            self.state.bot_detect_type = self.gui.return_bot_type_entry()
            inputs = {
                "current_year": str(datetime.now().year), 
                "website_URL": self.state.website_URL, 
                "web_type": self.state.web_type, 
                "bot_detect_type":self.state.bot_detect_type,
                "topic":"web bots",
                "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"
            }
            # 4/16/2026 (edit): What I also noticed here is that the msg_Queue above follows the code LINE BY LINE.
            #   So, this .put operation should logically be above the inputs mode.
            self.gui.msg_Queue.put("Agents Launched!\nAgents now analyzing website....\nPlease wait for final results....")
            msgOutput = self.gui.msg_Queue.get_nowait()
            self.gui.message_Stream(f"{msgOutput}")

            crew = BotDetectionOrche().crew()

            # --- DANGER: ADD THESE FOR DEBUGGING ONLY ---
            #print("-" * 50)
            #print("DEBUG CHECK: Data passed to Agents:")
            #print(f"Website URL: {self.state.website_URL}")
            #print(f"Web Type: {self.state.web_type}")
            #print(f"Bot Detect Type: {self.state.bot_detect_type}")
            #print("-" * 50)
            #web_urll = getattr(self.gui, "return_URL_Entry", lambda: "")()
            #print("web_Url:", web_urll)
            # --- END DEBUGGING ---
            # With the debugging, it seems that the agents have empty values.

            agents_Assemble = crew.kickoff(inputs=inputs)

            raw = getattr(agents_Assemble, "raw", None)
            #self.state.results = agents_Assemble.raw
            self.state.results = f"Agent results: {raw if raw is not None else str(agents_Assemble)}"
            #self.main_gui.message_Stream(f"Here's what we got:{self.state.results}")

            self.gui.msg_Queue.put(f"Agents website analysis complete!\nHere's what we got: {self.state.results}")
            self.gui.message_Stream(self.gui.msg_Queue.get_nowait())
        except Exception as e:
            self.state.results = f"Agent execution failed: {e}"
            self.gui.msg_Queue.put(f"🚨 FAILURE: Agent execution failed. Details{e}")
            self.gui.message_Stream(self.gui.msg_Queue.get_nowait())
            #self.main_gui.message_Stream(self.state.results)
        return self.state.results
    # Input Operation GUI ends here.

# OLD METHOD.
#def agents_thread(self, website_URL= None, web_type = None, bot_detect_type = None):
    #thread = threading.Thread(target=Guide_Web_Bot_Flow().input_Operation())
    #thread.start()
#    self.website_URL = website_URL
#    self.web_type = web_type
#    self.bot_detect_type = bot_detect_type
    # 3/30/2026: Copied from the input_operation listener function.
    
#    self.main_gui.message_Stream("Now onto the Agentic Phase...")
    # Calls the Agents and gives the website URL, web type, and bot detect type from the GUI, and to the agents to start analyzing a webpage.
#    agents_Assemble = BotDetectionOrche().crew().kickoff(inputs={"current_year": str(datetime.now().year), "website_URL": self.website_URL, 
#                                                                "web_type": self.web_type, 
#                                                                "bot_detect_type":self.bot_detect_type,
#                                                                "topic":"web bots",
#                                                                "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"})
#    self.main_gui.message_Stream("Looking at the website...")
    
#    lock.acquire() # acquires elements from the threads, specifically responses and inputs (in understanding so far.)
#    lock.release() # releases the lock and allows another thread for operations.
#    self.results = agents_Assemble.raw
#    self.main_gui.message_Stream(f"Here's what we got: {self.results}")

#----------------
# NEW CODE: GUI controller
#----------------

class AppController:
    # ------------------ Initialized App function starts here.
    def __init__(self, root: tk.Tk):
        """Initialize a app controller using the WebBotWindow superclass."""
        self.root = root
        # This reuses the superclass WebBotWindow from the WebBotGUI.py file.
        self.gui = WebBotWindow()

        # Submit button: This here BINDS the submit button to a wrapper, which
        #   makes the Submit button actually start the flow.
        try:
            # While the Submit Button is on the GUI, assume that it works and commands the agents once clicked.
            self.gui.message_Stream("Greetings from Web Bots!\n This tool will help you check on a website's bot traffic." \
            "\nThis Tool can also let you check good bots, nefarious bots, or both on a site while " \
            "giving you info on them! \nEnter the URL, Website Type, and Bot_type to Start!")
            self.gui.submit_button.config(command=self.during_submit)
            #if()
        except Exception:
            # Otherwise, the override button command from WebBotWindow is used to call the agents thread.
            if hasattr(self.gui, "override_button_command"):
                self.gui.override_button_command(return_agents_Thread=self.during_submit)
        self.agents_worker_thread = None
    # --------------- Initialized App function ends here.

    # --------------- collection_state_gui() function starts here.
    def collection_state_GUI(self) -> Optional[Guide_Web_Bot_State]:
        """Acts as the extension of the get_user_input method, where it retrives entries
        and has the submit button to rely with."""
        # Fetches the entries from the gui by using the gui class attributes.
        #while(not ""):
        #    get_URL_entry = self.gui.return_URL_entry()
        #    get_web_type_entry = self.gui.return_web_type_entry()
        #    get_bot_type_entry = self.gui.return_bot_type_entry()
        #    break

        #url_Entry = getattr(self.gui, "return_URL_Entry", lambda: "")()
        #web_Type_Entry=  getattr(self.gui, "return_web_type_entry",lambda:"")()
        #bot_Type_Entry = getattr(self.gui, "return_bot_type_entry", lambda: "")()

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
        """Once the Submit Button is clicked, the flow starts in a background thread."""
        # Uses the input states from the GUI.
        state = self.collection_state_GUI()

        # GUI responds to the input.
        try:
            self.gui.message_Stream("Okay, Agents Assemble!")
            self.gui.lock_Submit_Input() # Locks the submit input button upon succesful inputs.
        except Exception:
            pass
        # Now, a thread for the agents is made here.
        self.agents_worker_thread = threading.Thread(target= self._agent_flow_worker, 
                                              args= (state,), daemon = True)
        # The reason args is set to state is because of flows nature on relying on states to proceed through
        #   steps in code bodies to the end.
        self.agents_worker_thread.start() # Starts the thread.
    # ----------------During_Submit() function ends here.

    # agent_flow_worker() function starts here
    def _agent_flow_worker(self, state: Guide_Web_Bot_State): # Utilizes the newly retrieve inputs from the GUI while being states.
        """Acts as a worker for the Flow, where it runs the Flow while also updating the GUI."""
        # state=state means that the new state is equal to the entries retrived and set in Guide_Web_Bot_State.
        flow = Guide_Web_Bot_Flow(state=state, gui=self.gui)
        # This here runs the flow synchronously (which blocks only the agents_worker_thread).
        
        try:
            # Stores the result while starting flow via run function. Otherwise, it uses the .kickoff function.
            #  This program, however, uses the Flow API, so it uses .kickoff instead.
            #result = getattr(flow, "run", None)
            if hasattr(flow, "run"):
                flow.run()
                self.gui
            else:
                flow.kickoff()
                #self.gui.root.after(0, lambda: self._update_gui(flow.state))
                self.gui.msg_Queue.put(f"{flow.state}")
                self.gui.root.after(0, lambda: self.gui.refreshWindow(self.gui.msg_Queue.get_nowait()))
        except Exception as e:
            flow.state.results = f"Flow operation failed. {e}"
        # Schedule GUI update on main thread
        final_text = flow.state.results or "No results."
        #self.gui.refreshWindow(final_text) # Refreshes the window with new text.
        #self.root.after(0, lambda: self._update_gui(final_text))
        self.gui.msg_Queue.put(f"{final_text}") # Safely puts the final text (formatted) in the msg_Queue.
        format_Final = self.gui.msg_Queue.get_nowait() # Safely gets the final text (since it is the first in line here).
        self.gui.root.after(0, lambda: self.gui.refreshWindow(format_Final))
        
    # agent_flow_worker ends here.    

    #def _update_gui(self, text: str):
    #    """Safely updates the GUI."""
    #    try:
    #        if hasattr(self.gui, "msg_Queue"):
    #            self.gui.msg_Queue.put(text)
    #        else:
    #            self.gui.message_Stream(text)
    #        self.gui.unlock_Submit_Input()
    #    except Exception:
    #        pass

    #def _update_gui(self, text: str):
    #    """Safetly updates the GUI with the final result."""
    #    self.gui.refreshWindow(text)

# Runs the Guide Web Bot Flow class.
def kickoff():
    # Old Code:
    #bot_flow = Guide_Web_Bot_Flow()

    # New Code:
    root = tk.Tk()
    root.withdraw() # Prevents a duplicate window.
    app = AppController(root)

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
#    global_GUI = WebBotWindow("Hello, Enter the fields to start!",start_flow_callback=start_flow_thread)
#    global_GUI.run_main_loop() # runs the main window.
# Class ends here.