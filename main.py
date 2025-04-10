import streamlit as st
import sys
import os
# from agents.auto import AutomationAgent
# from agents.think import thinkModel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from agents.combined import combinedModel

input_data = st.text_area("input")
def clean(data):
    return data
parsed_data = clean(input_data) # Some function you've made to clean the input data

output = st.text_area("parsed data", value=parsed_data)


# # Streamlit Page Configuration
# st.set_page_config(layout="wide")
# MODELS = ['gemma2-9b-it','llama-3.3-70b-versatile', 'llama-3.1-8b-instant', "mixtral-8x7b-32768", "qwen-2.5-coder-32b", "deepseek-r1-distill-llama-70b"]

# # Sidebar settings
# with st.sidebar:
#     st.title("Settings")
#     model = st.selectbox("Model", MODELS)

# # Check if model is initialized, otherwise initialize
# if 'agent' not in st.session_state:
#     with st.spinner("Initializing model..."):
#         # Initialize the model only if it's not already done
#         st.session_state.agent = combinedModel()

# # Fetch the initialized agent
# agent = st.session_state.agent

# # Input and button for command
# query = st.text_input("Command")
# start = st.button("Start Automation")

# # Handle button click
# if start:
#     with st.spinner("Running..."):
#         # Execute the agent's call method with the query
#         agent.call(query)