import streamlit as st
import streamlit.components.v1 as components

url = "https://www.fourpaws.ai/gr"
url2 = "https://www.fourpaws.ai/gr2"
# embed streamlit docs in a streamlit app
#components.iframe(url, height=600, width=800)

# Create a markdown link that opens in a new tab
link = f'<a href="{url}" target="_blank">Open GazeRecorder1 in new window</a>'
link2 = f'<a href="{url2}" target="_blank">Open GazeRecorder2 in new window</a>'

# Display the link
st.markdown(link, unsafe_allow_html=True)
st.write(' ')
st.markdown(link2, unsafe_allow_html=True)
