# Personal-News-Curator-using-CrewAI
Personal News Curator let's you select a topic from a given set of fields, and provides you a concised summary of news articles and publications made regarding the same in the last 24 hours. It also provides a list of resources it referred as well as direct links to them.
It uses SerperAPI to search different news articles regarding the selected topic available across the internet. It filters the news articles that were published in the last 24 hours and creates a concised summary of multiple such articles.
The .env file contains the API keys used in this project to access external resources.
agents.py file defines two agents, news researcher and news summarizer that performs the two most important tasks of the project.
config.toml is required for streamlit styling
task.py defines the task to be performed by the LLM and provides the structure of the output expected.
tools.py integrates the SerperAPI tool for Web Scrapping different articles and news available on the internet.
crew.py integrates all the files together.
streamlit_app.py draws the frontend User Interface of the project.
