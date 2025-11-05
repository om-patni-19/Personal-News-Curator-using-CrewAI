# Updated file: task.py

from crewai import Task
from tools import search_tool, scrape_tool  # We still import scrape_tool
from agents import news_research, news_summary_agent

# Research task: NEW STRATEGY
research_task = Task(
    description=(
        "Collect and analyze the most relevant news stories from the past 24 hours about {topic}. "
        "First, use the search tool to find 3-4 promising article URLs. "
        
        # --- THIS IS THE NEW INSTRUCTION ---
        "IMPORTANT: The search tool will return a list of results, each with a 'snippet', 'title', and 'url'. "
        "Do NOT use the scrape tool. It is unreliable and will get blocked. "
        "You MUST synthesize your summary *directly* from the 'snippet' of each search result."
    ),
    expected_output=(
        "A Python dictionary string with two keys: "
        "1. 'summary': A detailed, synthesized report of all findings, based *only* on the snippets from the search results. "
        "2. 'sources': A list of dictionaries, where each dictionary has 'title' and 'url' keys for each search result."
    ),
    tools=[search_tool],  # <--- CRITICAL: REMOVED scrape_tool FROM THE LIST!
    agent=news_research,
)

# Write task: (No changes needed here)
write_task = Task(
    description=(
        "Review the research report provided on {topic}. "
        "Condense the report's 'summary' key into a clear, concise news summary (under 250 words). "
        "You MUST pass along the 'sources' list from the report *unmodified* in your final output."
    ),
    expected_output=(
        "A single, final JSON string with two keys: "
        "1. 'final_summary': The polished, concise news summary. "
        "2. 'final_sources': The original list of source dictionaries (each with 'title' and 'url')."
    ),
    tools=[], 
    agent=news_summary_agent,
    context=[research_task],
    async_execution=False,
)