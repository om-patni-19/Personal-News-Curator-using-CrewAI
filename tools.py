# https://serper.dev/api-keys 

from dotenv import load_dotenv
import os

load_dotenv() 
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# Tool for searching - THIS IS THE FIX
# We are setting the tool to be a 'news' search tool by default.
search_tool = SerperDevTool(search_type='news')

# We'll leave the scrape tool here, but we're going to tell the agent not to use it.
scrape_tool = ScrapeWebsiteTool()
