# Updated file: streamlit_app.py
# Description: Includes the function to load a local background image.

from crewai import Crew, Process
from task import research_task, write_task
from agents import news_research, news_summary_agent

import streamlit as st
import json
from dotenv import load_dotenv
import os
import base64 # Import base64

# Load environment variables
load_dotenv()

# --- Helper Function for Background Image ---
# --- NEW: Helper Function for Background Image (More Robust) ---
def add_bg_from_local(image_file):
    """
    Sets a local image as the app's background.
    This version uses more stable selectors and !important to override the theme.
    """
    try:
        with open(image_file, "rb") as image_file_obj:
            encoded_string = base64.b64encode(image_file_obj.read()).decode()
        
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Make the main content area transparent */
            [data-testid="stAppViewContainer"] > .main {{
                background-color: transparent !important;
            }}

            /* Make the sidebar semi-transparent */
            [data-testid="stSidebar"] > div:first-child {{
                background-color: rgba(14, 17, 23, 0.85) !important; /* Adjust darkness/opacity */
            }}

            /* Target all containers, cards, and tab containers */
            [data-testid="stVerticalBlockBorderWrapper"] {{
                background-color: rgba(46, 51, 60, 0.85) !important; /* Adjust darkness/opacity */
                border-radius: 10px; /* Optional: adds a nice rounded corner */
            }}
            
            /* Target the tab bar itself */
            [data-testid="stTabs"] {{
                background-color: transparent !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("Background image 'background.png' not found. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred while setting the background: {e}")

# --- Page Configuration ---
st.set_page_config(
    page_title="Tech News CrewAI App",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Call the background function ---
# This will look for 'background.png' in the same directory
add_bg_from_local('background.png') 

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    topics = [
        "Artificial Intelligence",
        "Blockchain & Cryptocurrency",
        "Quantum Computing",
        "Space Exploration",
        "Biotechnology",
        "Cybersecurity",
        "Renewable Energy",
    ]
    topic = st.selectbox("Choose a news topic:", topics)

    generate_button = st.button("Summarize News", type="primary", use_container_width=True)

    st.markdown("---")
    
    with st.expander("ℹ️ How it works"):
        st.markdown(
            """
            1.  **Select a topic** from the dropdown.
            2.  **Click 'Summarize News'**.
            3.  The **Researcher Agent** scans the web.
            4.  The **Summarizer Agent** writes a concise report.
            5.  View your results in the organized tabs.
            """
        )

# --- App Header (PERSISTENT) ---
col1, col2 = st.columns([1, 10]) 
with col1:
    st.markdown("<h1 style='font-size: 60px; text-align: center; margin-top: -20px;'>📰</h1>", unsafe_allow_html=True) 

with col2:
    st.title("Tech News Summarizer")
    st.markdown("Your AI-powered briefing on the latest in tech.")


# --- Main Crew Logic Function ---
@st.cache_data(show_spinner=False) 
def generate_news_summary(topic):
    """
    Kicks off the CrewAI crew to generate the news summary.
    """
    tech_news_crew = Crew(
        agents=[news_research, news_summary_agent],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=False
    )
    result = tech_news_crew.kickoff(inputs={"topic": topic})
    return result

# --- Main App Body ---

# 1. Logic for the "Empty State"
if not generate_button:
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>Welcome!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.1em;'>I'm ready to research the latest tech news for you.</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Please select a topic from the sidebar on the left and click <strong>'Summarize News'</strong> to begin.</p>", unsafe_allow_html=True)
        
        st.markdown("\n\n")
        # 
        st.markdown("\n")


# 2. Logic for the "Results State"
if generate_button:
    if not topic:
        st.warning("Please choose a topic from the sidebar first.")
    else:
        with st.spinner(f"🚀 CrewAI is researching '{topic}'... This may take a moment."):
            try:
                crew_output = generate_news_summary(topic)
                
                # --- Parse the JSON output ---
                raw_json_string = crew_output.raw 
                result_data = None
                
                try:
                    start_index = raw_json_string.find('{')
                    end_index = raw_json_string.rfind('}') + 1
                    
                    if start_index != -1 and end_index != -1:
                        json_part = raw_json_string[start_index:end_index]
                        result_data = json.loads(json_part)
                    else:
                        st.error("Error: Could not find a valid JSON object in the crew's output.")
                        st.code(raw_json_string) 
                
                except json.JSONDecodeError as e:
                    st.error(f"Error: Failed to parse the crew's output. {e}")
                    st.code(raw_json_string)
                except AttributeError:
                    st.error("Error: The crew did not return a valid string output.")
                    st.code(crew_output)

                # --- Display the parsed output (Using Tabs) ---
                if result_data:
                    st.header(f"📈 Your Briefing on: {topic}", divider='rainbow')
                    
                    tab_summary, tab_sources = st.tabs(["📝 Summary", "🔗 Sources",])

                    with tab_summary:
                        with st.container(border=True):
                            st.markdown(result_data.get('final_summary', "No summary was generated."))

                    with tab_sources:
                        with st.container(border=True):
                            st.subheader("Clickable Source Articles")
                            sources = result_data.get('final_sources', [])
                            
                            if sources:
                                for source in sources:
                                    title = source.get('title', 'Source Link')
                                    url = source.get('url')
                                    if url:
                                        st.markdown(f"- [{title}]({url})")
                            else:
                                st.info("No source articles were found for this summary.")
                            
                            st.markdown("---") 
                            
                            md_output = f"### Summary for: {topic}\n\n"
                            md_output += f"{result_data.get('final_summary', 'N/A')}\n\n"
                            md_output += "### Sources\n\n"
                            if sources:
                                for source in sources:
                                     md_output += f"- [{source.get('title', 'Source Link')}]({source.get('url')})\n"
                            else:
                                md_output += "No sources found.\n"

                            st.download_button(
                                label="Download Summary (.md)",
                                data=md_output,
                                file_name=f"{topic.lower().replace(' ','_')}_summary.md",
                                mime="text/markdown",
                                use_container_width=True
                            )

            except Exception as e:
                st.error(f"An error occurred while running the crew: {e}")
                
# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Built with CrewAI, Google Gemini, and Streamlit 🚀</div>", unsafe_allow_html=True)