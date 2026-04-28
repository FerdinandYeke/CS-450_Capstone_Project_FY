from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool
# from crewai_tools import WebsiteSearchTool
# from crewai_tools import OxylabsUniversalScraperTool
# from crewai_tools import SeleniumScrapingTool
from typing import List
from crewai_tools import SpiderTool
# 2/18/2026 Edit: Before, this orginally used gpt-4o-mini, but this will
# use the LLM framework Ollama, with the llm that it will use being gemma 3 of 4b model.
from crewai import LLM
from crewai.project import CrewBase, agent, crew, task, llm

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BotDetectionOrche():
    """BotDetectionOrche crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # --Originally, this was meant to be in a hierarchical structure. Due to complexity on agents, a sequential stucture is followed instead.
    # --With this sequential structure, the Web Bot Researcher Agent runs first (to research and gather up-to date info for the other agents). 
    #       The Context Pattern Seeker Agent runs second (to see any signs and patterns of bots in the given website with the Spider Scraper tool), and the Reporting Analyst
    #       Agent running last (which builds a comprehensive report on the agents findings.).
    @agent
    # --Researcher Agent function starts here
    def researcher(self) -> Agent:
        """ Defines the researcher function as an agent. Otherwords, this sets up the Researcher agent."""
        # --Instantiated SerperDevTool into variable search_tool.
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            memory= True,
            max_iter= 15,
            max_retry_limit=3,
            tools= [search_tool]
        )
    # --Researcher Agent function ends here.

    @agent
    # --Context Pattern Agent function starts here.
    def context_pattern_agent(self) -> Agent:
        """"Like the other defined methods, this new method defines the context pattern agent."""
        # uni_ScraperTool= OxylabsUniversalScraperTool(
        #    config={
        #        "render": "html",
        #        "user_agent_type":"desktop",
        #        "url": "{website_URL}"
        #    }
        #)
        # -- For the Context Pattern Agent to actually look for potential bots in a website, the most fitting approach (currently) is using a web scraper tool Spider.
        #       With Spider, the Context Pattern Agent can look specifically at the HTTP elements and HTTP Requests of a website (while also being given context on what is
        #       a good/benificiary bot versus a malicious bot.) and see bots of type good or bad. 
        spider_tool = SpiderTool()
        return Agent(
            config=self.agents_config['context_pattern_agent'], # type: ignore[index]
            memory= True,
            # -- Here, this agent will use the Spider Scraper Tool,
            #     where it will scrape a website's info.
            tools= [spider_tool],
            max_iter= 15,
            max_retry_limit=3, # --Limits scraping attempts to 3.
            verbose=True
        )
    # --Context Pattern Agent function ends here.
    
    @agent
    # --Reporting Analyst Agent function starts here
    def reporting_analyst(self) -> Agent:
        """ Defines the reporting analyst function as an agent, i.e. setting up the Reporting analyst as an agent."""
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            memory= True,
            max_iter= 15,
            max_retry_limit=3,
            verbose=True
        )
    # --Reporting Analyst Agent function ends here. 

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def research_task(self) -> Task:
        """" This defines the research task as an actual Task for the Research Agent."""
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
        )

    @task
    def context_pattern_task(self) -> Task:
        """Sets up context_pattern_task as an actual task for the Context Pattern Seeker Agent.""" 
        return Task(
            config=self.tasks_config['context_pattern_task'] # type: ignore[index]
        )
    
    @task
    def reporting_task(self) -> Task:
        """ This defines the reporting task as an actual task for the Reporting Analyst Agent."""
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BotDetection crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            #process= Process.hierarchical,
            #manager_llm=LLM(model="ollama/gemma3:4b", base_url= "http://localhost:11434"),
            process= Process.sequential,
            #planning= True, 
            verbose=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
    # IMPORTANT! For local usage, an Ollama LLM framework with Gemma 3 will be used here.
    # Edit, now stored in the .env file.
#    @llm
#    def my_ollama_llm(self):
#        """Constructs the Ollama LLM."""
#        return LLM(model="ollama/gemma3:4b", base_url="http://localhost:11434")
    
