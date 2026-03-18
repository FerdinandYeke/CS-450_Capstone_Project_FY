#!/usr/bin/env python
from datetime import date
import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from crewai.agent import Agent
from datetime import datetime
# Imports the BotDetectionOrche class (short for Orchestration) in this main file.
from bot_flow.crews.bot_detection_orche.bot_detection_orche import BotDetectionOrche

# Imports the web_Bot GUI class
from bot_flow.web_bot_main_wind_new import WebBotWindow

import threading

# 3/4/2026: The web bot window class will be planned to be imported into this class.

# Firstly, the flow state will be defined with related objects.

class Guide_Web_Bot_State(BaseModel):
    web_type: str = ""
    topic: str = ""
    bot_detect_type: str = ""
    website_URL: str = ""
    results: str = ""
    current_year: datetime = ""
    current_date: datetime = ""
    # current_year: date.year 
class Guide_Web_Bot_Flow(Flow[Guide_Web_Bot_State]):
    """This is a flow for making a bot detection on a website."""
    # Calls the super class from WebBotWindo
    #def __init__(self, gui_instance):
    #    super().__init__()
    #    self.gui = gui_instance
    # Super class call & function ends here.
    @start()
    # Get User Input GUI method/function starts here.
    def get_user_input_GUI(self):
        """This gets input from the user, where this input is a URL that checks to see bots in the website.
        * Instead of getting inputs by terminal like the main_OLD.py file, this does it via GUI."""
        self.global_GUI = WebBotWindow(start_flow_callback=start_flow_thread())
        #self.global_GUI.construct_widgets("Enter Text: ")
        self.global_GUI.message_Stream("Hello, Enter the fields to start detecting bots!")
        #self.global_GUI.run_main_loop() # runs the main window.
       # start_messages = (
       #     (f"Checking out the website {self.state.website_URL} while considering the web type {self.state.web_type} and {self.state.bot_detect_type} bots..."
       #       "\n Please Wait...")
       # )
        # If gui is actually open and working, the messages above will print out in the text box.

       # if self.global_GUI:
        #    self.global_GUI.message_Stream(start_messages)
        #print(start_messages)
        return self.state
    
    # Based of the build your first flow with the GuideCreaterFlow Example Class.
    @listen(get_user_input_GUI)
    def input_Operation(self, state):
        """Agents run off of the user's input."""
        # In this method, the agents will be planned to be called here to handle the link.
        self.global_GUI.run_main_loop() # runs the main window.
        # Here, the agentic phase will be noted in the GUI as well.
        if self.global_GUI:
            self.global_GUI.message_Stream("Now onto the Agentic Phase...")
        # Old Code:
        #agents_Assemble = BotDetectionOrche().crew().kickoff(inputs={"current_year": str(datetime.now().year), "website_URL": self.state.website_URL, 
        #                                                             "web_type": self.state.web_type, 
        #                                                             "bot_detect_type":self.state.bot_detect_type,
        #                                                             "topic":"web bots",
        #                                                             "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"})
        # Prints out what the Agents discovered onto the GUI text box.

        # New Code:
        if(self.global_GUI.return_bot_type_entry != "" & self.global_GUI.return_URL_entry != "" & self.global_GUI.return_web_type_entry != ""):
            self.state.website_URL = self.global_GUI.return_URL_entry()
            self.state.web_type = self.global_GUI.return_web_type_entry()
            self.state.bot_detect_type = self.global_GUI.return_bot_type_entry()
            self.global_GUI.submit_input
            agents_Assemble = BotDetectionOrche().crew().kickoff(inputs={"current_year": str(datetime.now().year), "website_URL": self.state.website_URL, 
                                                                        "web_type": self.state.web_type, 
                                                                        "bot_detect_type":self.state.bot_detect_type,
                                                                        "topic":"web bots",
                                                                        "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"})

        self.state.results = agents_Assemble.raw
        #print("Here's what we got: ", self.state.results)

        if self.global_GUI:
            self.global_GUI.message_Stream(f"Here's what we got: {self.state.results}")
        return self.state
    # Input Operation GUI ends here.

# Running Agentic Flow function starts here.
# Basically, this function makes sure that the inputs from the user are recieved from the GUI,
#   as if it were from the terminal.
def running_agentic_flow(user_data, msg_Queue):
    """This function runs within the background thread."""
    try:
        # 1. First, the Flow instance is made to the GUI reference.
        #    This also is where the GUI object can be accessed.
        bot_flow = Guide_Web_Bot_Flow()

        # 2. Next, the dictionary values gets set up here and stored in the state variables.
        bot_flow.state.website_URL = user_data["website_url"]
        bot_flow.state.web_type = user_data["website_type"]
        bot_flow.state.bot_detect_type = user_data["bot_type"]
         # 3. Finally, the Flow starts. If there is an error, it will not start and will
         #  instead print out an exception error.
        result= bot_flow.kickoff()
        result
        msg_Queue.put(f"Final Results{result}")
    except Exception as InputException:
        msg_Queue.put(f"Error: {str(InputException)}")
# Running Agentic Flow function ends here.

# Start flow thread function starts here.
def start_flow_thread():
    """Makes the flow without the GUI being blocked, but synced instead"""
    thread = threading.Thread(target=Guide_Web_Bot_Flow())
    thread.daemon = True # Closes once the GUI itself close.
    thread.start()

# Runs the Guide Web Bot Flow class.
def kickoff():
    # Old Code:
    #bot_flow = Guide_Web_Bot_Flow()

    # New Code:
    bot_flow = Guide_Web_Bot_Flow()
    bot_flow.kickoff()
# Plots the Guide Web Bot Flow class.
#def plot():
#     bot_flow = Guide_Web_Bot_Flow()
#     bot_flow.plot("WebBotFlowPlot")
# Executes both the kickoff and plot functions.
if __name__ == "__main__":
    kickoff()
    # 3/3/2026: Plot will be done later.
#    plot()

    # Finally, once the kickoff starts, the gui does as well.
#    global_GUI = WebBotWindow("Hello, Enter the fields to start!",start_flow_callback=start_flow_thread)
#    global_GUI.run_main_loop() # runs the main window.
# Class ends here.