# AI Code Generator

This Streamlit app uses Google's Generative AI (Gemini) to generate code from a prompt, 
then fetches relevant YouTube tutorials based on the functions found in the code.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shiv1909/my_app.git

2. Navigate into the directory:
    ```bash
    cd my_app

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    .\venv\Scripts\activate   # On Windows

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

5. Create a .env file in the root directory with your keys:
    ```ini
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY

6. Run the Streamlit app:
    ```bash
    streamlit run app.py
