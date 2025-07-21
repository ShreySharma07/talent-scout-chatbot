# TalentScout Hiring Assistant 🤖

## Project Overview
This project is an intelligent Hiring Assistant chatbot for "TalentScout," a fictional recruitment agency. The chatbot is designed to conduct initial candidate screenings by gathering essential information and asking technical questions based on the candidate's declared tech stack. The application is built with Python and Streamlit and leverages a Large Language Model (Google's Gemini) for its conversational intelligence.

---

## Technical Details
* **Language:** Python 3.12
* **UI Framework:** Streamlit 
* **LLM:** Google Gemini 2.5 Flash (via the `genai` library) 
* **Architecture:** The application operates as a state machine, managed within Streamlit's `session_state`. This ensures a logical and context-aware conversation flow, from greeting and information gathering to technical questioning and closing.

---

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd talent-scout-chatbot
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up API Key:**
    * Create a file at `.streamlit/secrets.toml`.
    * Add your Google AI Studio API key: `GEMINI_API_KEY = "your-key-here"`

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

---

## Prompt Design
Effective prompts are crucial for guiding the LLM. Here's how they were designed:

* **Information Gathering:** The `INFO_GATHERING_PROMPT_TEMPLATE` instructs the LLM to act as an expert hiring assistant with a clear list of required details. It is provided with the full chat history to maintain context. Most importantly, it is designed to return a special keyword, `ALL_INFO_GATHERED`, which acts as a signal to the application to transition to the next stage. This creates a reliable, programmatic way to advance the conversation.

* **Technical Question Generation:** The `QUESTION_GENERATION_PROMPT_TEMPLATE` is given a specific role ("expert technical interviewer") and a clear task: generate 3-5 questions based *only* on the tech stack declared by the candidate during the conversation. This ensures the questions are relevant and tailored.

---

## Challenges & Solutions
* **Challenge:** Maintaining a coherent, multi-step conversation. A simple chatbot can forget the context between user inputs.
* **Solution:** I implemented a state machine using Streamlit's `st.session_state`. A `stage` variable tracks the conversation's progress (Greeting, Info Gathering, etc.). The application's logic checks this `stage` before deciding how to process user input and which prompt to use, ensuring the chatbot never loses its place.

---

## Bonus Features Implemented
* **Sentiment Analysis:** To gauge candidate emotions, a secondary LLM call is made after each user input. A specialized prompt classifies the input as POSITIVE, NEGATIVE, NEUTRAL, or CONFUSED, and the result is displayed in the UI.
* **UI Enhancements:** The Streamlit interface's aesthetic appeal was improved using custom CSS injected via `st.markdown`. This provides a more professional look with custom colors and spacing.
