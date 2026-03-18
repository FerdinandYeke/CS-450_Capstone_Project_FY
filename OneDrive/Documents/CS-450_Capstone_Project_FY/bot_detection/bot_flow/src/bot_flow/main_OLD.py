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
    @start()
    # Window will be planned to be called here.
    def get_user_input(self):
        final_wb_window = WebBotWindow("Greetings from Web Bots!\n This tool will help you check on a website's bot traffic." \
        "\nThis Tool can also let you check good bots, nefarious bots, or both on a site while " \
        "giving you info on them! \nEnter the URL to Start!").run_main_loop()
        
        #"""This gets input from the user, where this input is a URL that checks to see bots in the website."""

        print("Greetings from Web Bots!\n This tool will help you check on a website's bot traffic." \
        "\nThis Tool can also let you check good bots, nefarious bots, or both on a site while " \
        "giving you info on them! \nEnter the URL to Start!")
        
        #WB_Window.message
        
        #WB_Window.setWindow()
        #WB_Window.text_Output(intro_text)

        # First, this gets the user's input.
        set_web_URL = input("(Enter the URL): ")
        #wb_Window.url_entry_widget = set_web_URL
        self.state.website_URL = set_web_URL
        self.state.website_URL = final_wb_window.url_entry_widget

        # Next, checks if the website is a Social Media Site or a E-Commerce Site.
        set_web_type = input("What is the website's type? Is it Social Media or E-Commerce? \n"
        "(Enter social_media for Social Media, or Enter e-commerce for E-Commerce.): ")

        # 3/3/2026: This will also be planned to have a GUI button pop-up selecting the web type. This will also try to correct itself if
        # The web type selected by the user is not correct, while an agent could figure that out. (THIS WILL PLAN TO HAVE GUARDRAILS.)
        if (set_web_type == "social_media" or "e-commerce"):
            final_wb_window.web_type_entry = set_web_type
            self.state.web_type = set_web_type
            self.state.web_type = final_wb_window.web_type_entry
            print("The website type you have selected is: ", set_web_type,"!")
            final_wb_window.message_Output(f"The website type you have selected is: ", {set_web_type},"!")

        # Setting Bot Type: After website type, this gets the user's input on what bot to detect.

        # THIS will plan to have guardrails to PROTECT the good bots of the site.
        set_bot_type = input("What types of Robots do you want to view? \n(Enter" \
        " good_bots for Good bots, or bad_bots for Nefarious Bots): ")
        # This checks to see if the inputs are good bots or bad bots. Will try to do a try/catch for any other
        # invalid inputs.
        if(set_bot_type == "good_bots" or "bad_bots"):
            final_wb_window.bot_type_entry = set_bot_type
            self.state.bot_detect_type = set_bot_type
            self.state.bot_detect_type = final_wb_window.bot_type_entry
            print(f"The Bot type you have selected is: {self.state.bot_detect_type}!") # This might change to just the set_bot_type variable instead.
            final_wb_window.message_Output(f"The Bot type you have selected is: !")

        final_wb_window.submit_button
        final_wb_window.submit_input
        print(f"Checking out the website {self.state.website_URL} while considering the web type {self.state.web_type} and {self.state.bot_detect_type} bots..."
              "\n Please Wait...")
        # Reports it's state to other functions after operation is finished here.
        final_wb_window.message_Output(f"Checking out the website {self.state.website_URL} while considering the web type {self.state.web_type} and {self.state.bot_detect_type} bots..."
              "\n Please Wait...")
        return self.state
    
    # Based of the build your first flow with the GuideCreaterFlow Example Class.
    @listen(get_user_input)
    def input_Operation(self, state):
        """Agents run off of the user's input."""
        # In this method, the agents will be planned to be called here to handle the link.
        
        agents_Assemble = BotDetectionOrche().crew().kickoff(inputs={"current_year": str(datetime.now().year), "website_URL": self.state.website_URL, 
                                                                     "web_type": self.state.web_type, 
                                                                     "bot_detect_type":self.state.bot_detect_type,
                                                                     "topic":"web bots",
                                                                     "current_date":f"{(datetime.now().strftime('%Y-%m-%d'))}"})
        # Prints out what the Agents discovered.

        self.state.results = agents_Assemble.raw
        print("Here's what we got: ", self.state.results)
        final_wb_window.message_Output(self.state.results)
        #pass
# Runs the Guide Web Bot Flow class.
#def kickoff():
#    bot_flow = Guide_Web_Bot_Flow()
#    bot_flow.kickoff()
# Plots the Guide Web Bot Flow class.
#def plot():
#     bot_flow = Guide_Web_Bot_Flow()
#     bot_flow.plot("WebBotFlowPlot")
# Executes both the kickoff and plot functions.
#if __name__ == "__main__":
#    kickoff()
    # 3/3/2026: Plot will be done later.
#    plot()
# Class ends here.