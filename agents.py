# Updated file: agents.py

from crewai import Agent, LLM
from dotenv import load_dotenv
import os
from tools import search_tool, scrape_tool  # <-- Import BOTH tools

load_dotenv()  # Load environment variables from .env file

# Initialize the LLM with proper model name for Google's Gemini
llm = LLM(
    model="google/gemini-2.5-flash",
    temperature=0.5,
    api_key=os.getenv("GOOGLE_API_KEY")
)


news_research = Agent(
    role = "Senior Researcher",
    goal = "Collect and synthesize all news published in the past 24 hours about {topic}, highlighting ground-breaking technologies and trends.",
    verbose = True,
    memory = True,
    backstory = (
        "You are a highly skilled researcher specializing in emerging technologies. "
        "Your mission is to automatically gather, analyze, and condense the latest news updates from the past 24 hours, ensuring coverage of fresh developments and innovative breakthroughs in the field."
    ),
    tools = [search_tool, scrape_tool],  # <-- Give it BOTH tools
    llm = llm,
    allow_delegation = False,  # <-- STOP the pointless delegation
)


#creating a writing agent with custom tools responsible in writing news blog 

news_summary_agent = Agent(
    role = "News Summarizer",
    goal = "Summarize the research findings provided to you about {topic}",
    verbose = True,
    memory = True,
    backstory = (
        "You are an expert news summary agent, skilled at condensing complex research findings into clear, factual, and unbiased summaries. "
        "Your task is to extract key points and present critical news insights efficiently."
    ),
    tools = [],        # <-- Remove all tools. This agent ONLY summarizes.
    llm = llm,
    allow_delegation = False, 
)