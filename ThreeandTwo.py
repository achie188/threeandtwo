import pandas as pd
import streamlit as st

from inputs.pull_sportsdb import get_baseball_results
from pipeline.format_table import format_results



#Get data
baseball_results = get_baseball_results()


#Format the dataframe
formatted_bb = format_results(baseball_results)




# Set up Streamlit app
st.set_page_config(
    page_title="ThreeandTwo",
    layout="wide"
)


st.subheader("Welcome to the James' Three and Two Baseball Results")

st.write("The below shows results from the 2023 MLB Season 👇")

st.dataframe(formatted_bb, height=1000, hide_index=True)
