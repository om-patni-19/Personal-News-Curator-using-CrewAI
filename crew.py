from crewai import Crew, Process
from task import research_task, write_task
from agents import news_research, news_summary_agent
import json

# forming the tech-focused crew with some enhanced configurations

crew = Crew(
    agents=[news_research, news_summary_agent],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Agents will work on tasks one after another; alternative: Process.parallel
)

# Run the crew for five explicit domains and collect per-domain results
"""domains = [
    "Politics and International Relations",
    "Economy",
    "Finance",
    "Health",
    "Sports",
]

all_results = {}
for domain in domains:
    print(f"--- Running crew for domain: {domain} ---")
    try:
        res = crew.kickoff(inputs={"topic": domain})
    except Exception as e:
        # Capture exceptions per-domain so one failure doesn't stop the whole run
        res = {"error": str(e)}
    all_results[domain] = res

print("Crew Execution Results by domain:")
print(json.dumps(all_results, indent=2, ensure_ascii=False))"""

result = crew.kickoff(inputs={'topic': 'Finance'})
print("Crew Execution Result:", result)



