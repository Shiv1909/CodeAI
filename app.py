import streamlit as st
import google.generativeai as genai
import re
import requests
import os
from dotenv import load_dotenv
from prompt import Prompt, extracted_function

# Load environment variables
load_dotenv()

# Initialize Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in .env file. Please add it.")
    st.stop()

# Initialize YouTube Data API Key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    st.error("YOUTUBE_API_KEY not found in .env file. Please add it.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_code(prompt, language):
    system_prompt = Prompt(language)
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(system_prompt + prompt)
    return response.text if response else "Failed to generate code."

def Terms(code):
    model = genai.GenerativeModel("gemini-1.5-pro")
    system_prompt = extracted_function(code)
    response = model.generate_content(system_prompt)
    output_text = response.text
    # Clean up lines
    output_list = [
        re.sub(r'^\d+\.\s*', '', line) for line in output_text.splitlines() if line.strip()
    ]
    return output_list

def fetch_youtube_videos(queries, max_results=5):
    """
    Returns a list of tuples: [(title, video_url), (title2, video_url2), ...]
    """
    video_info = []
    base_url = "https://www.googleapis.com/youtube/v3/search"

    for query in queries:
        if len(video_info) >= max_results:
            break  # Stop once we have enough results

        params = {
            "part": "snippet",
            "q": query,
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
            "type": "video"
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            items = response.json().get("items", [])
            if items:
                title = items[0]["snippet"]["title"]
                video_id = items[0]["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_info.append((title, video_url))
        else:
            st.error(f"Error fetching YouTube videos for '{query}': {response.status_code}")

    return video_info

def process_prompt(prompt, language):
    # 1) Generate code
    generated_code = generate_code(prompt, language)

    # 2) Extract function names
    function_names = Terms(generated_code)
    
    # 3) Build queries
    youtube_queries = [f"{language} {func} tutorial" for func in function_names][:5]

    # 4) Fetch videos
    youtube_videos = fetch_youtube_videos(youtube_queries)

    # 5) Display the generated code
    st.markdown(f"```{language.lower()}\n{generated_code}\n```")

    # 6) Display the YouTube links in a bulleted list
    if youtube_videos:
        st.markdown("### :movie_camera: YouTube Tutorials")
        for title, url in youtube_videos:
            st.markdown(f"- [{title}]({url})")
    else:
        st.markdown("*No relevant YouTube videos found.*")

# Streamlit UI
st.title("💻 AI Code Generator")
st.markdown("### Generate beautifully formatted code from any prompt using Google Gemini.")

language = st.selectbox("Programming Language", ["Python", "JavaScript", "C++", "Java", "Go", "Rust"], index=0)
prompt_input = st.text_area("Enter your prompt", "Describe the functionality you need...", height=150)

if st.button("Generate Code"):
    with st.spinner("Generating code..."):
        process_prompt(prompt_input, language)
