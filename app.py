import streamlit as st
import requests
import json
from supadata import Supadata

supadata_api_key = st.secrets["supadata_api_key"]
glm_api_key = st.secrets["glm_api_key"]

llm_url = "https://api.z.ai/api/paas/v4/chat/completions"

supadata = Supadata(api_key=supadata_api_key)


# 1. --- Put your "get_summary" function here ---
# (This is the function you wrote in Colab that takes a link
#  and returns a summary string)
def get_summary_from_reel(instagram_url):
    transcript = supadata.transcript(url=instagram_url)
    #print(f"Got transcript {transcript.content}")

    payload = {
        "model": "glm-4.5-Flash",
        "messages": [
            {
                "role": "system",
                "content": "You are a useful AI assistant."
            },
            {
                "role": "user",
                "content": f"Please summarise and tell main points from this transcript: {transcript}"
            }
        ],
        "temperature": 1,
        "max_tokens": 65536,
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {glm_api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(llm_url, json=payload, headers=headers)

    response_json = response.json()
    if "choices" in response_json and response_json["choices"]:
        summary = response_json["choices"][0]["message"]["content"]
    else:
        print("Could not retrieve content from the response.")
        
    return summary
# -------------------------------------------------


# 2. --- Add the Streamlit UI (the webpage) ---
st.set_page_config(page_title="Reel Summarizer", layout="wide")
st.title("🎬 Instagram Reel Summarizer")
st.write("Paste a link to an Instagram Reel to get a quick text summary.")

# Get the URL from the user
reel_link = st.text_input("Enter the Instagram Reel URL:")

# Add a button
if st.button("Summarize"):
    if reel_link:
        # Show a loading spinner while your function runs
        with st.spinner("Hold on, summarizing the reel..."):
            try:
                # Run your function
                summary_text = get_summary_from_reel(reel_link)

                # Display the result
                st.subheader("Here's your summary:")
                st.success(summary_text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL first!")

