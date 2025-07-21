import streamlit as st
from google import genai
from google.genai import types
import prompts

st.set_page_config(page_title="TalentScout Assistant", page_icon="🤖")

st.markdown("""
<style>
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem;
    }
    .st-emotion-cache-1y4p8pa {
        padding-top: 2rem;
        max-width: 80%;
    }
    .st-emotion-cache-vj1c9o {
        background-color: #f0f2f6;
    }
    [data-testid="stChatMessageContent"] {
        background-color: #e8e8ff;
        border-radius: 0.5rem;
        padding: 0.8rem;
    }
    [data-testid="stChatInput"] {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    MODEL_NAME = "gemini-2.5-flash"

except Exception as e:
    st.error(f"Error initializing Google GenAI client: {e}. Please ensure your API key is set correctly in .streamlit/secrets.toml", icon="🚨")
    st.stop()


# --- STATE MANAGEMENT ---
CONVERSATION_STAGES = {
    'GREETING': 1,
    'INFO_GATHERING': 2,
    'QUESTIONING': 3,
    'CLOSING': 4
}
if 'stage' not in st.session_state:
    st.session_state.stage = CONVERSATION_STAGES['GREETING']
if 'messages' not in st.session_state:
    st.session_state.messages = []


# --- HELPER FUNCTIONS ---
def get_llm_response(prompt_text):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text
        )
        return response.text
    except Exception as e:
        st.error(f"An error occurred while communicating with the LLM: {e}")
        return None

def get_sentiment(text_input):
    """Analyzing the sentiment of the user's input."""
    prompt = prompts.SENTIMENT_ANALYSIS_PROMPT.format(user_input=text_input)
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception:
        return None

def get_chat_history_string():
    """Formats the chat history into a string for the LLM context."""
    history_string = ""
    for msg in st.session_state.messages:
        history_string += f"{msg['role'].capitalize()}: {msg['content']}\n"
    return history_string


# --- UI RENDERING ---
st.title("🤖 TalentScout Hiring Assistant")
st.write("I'm here to assist with the initial screening. Please answer a few questions.")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- MAIN CONVERSATION LOGIC ---
if st.session_state.stage == CONVERSATION_STAGES['GREETING']:
    greeting = prompts.GREETING_MESSAGE
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state.stage = CONVERSATION_STAGES['INFO_GATHERING']


# Main input and response loop
# if user_input := st.chat_input("Your response..."):
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)
if user_input := st.chat_input("Your response..."):
    # First, display the user's message in the chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- SENTIMENT ANALYSIS CALL (BONUS) ---
    # Now, outside the chat bubble, perform and display the sentiment analysis
    sentiment = get_sentiment(user_input)
    if sentiment:
        # The st.info tag now renders in the main app area
        st.info(f"Candidate Sentiment: {sentiment.strip()}", icon="😊")
    else:
        # This provides feedback if the sentiment analysis fails
        st.warning("Could not analyze sentiment for the last message.", icon="⚠️")


    if st.session_state.stage == CONVERSATION_STAGES['INFO_GATHERING']:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_prompt = prompts.INFO_GATHERING_PROMPT_TEMPLATE.format(
                    chat_history=get_chat_history_string(),
                    user_input=user_input
                )
                response = get_llm_response(full_prompt)
                if response:
                    if "ALL_INFO_GATHERED" in response:
                        st.session_state.stage = CONVERSATION_STAGES['QUESTIONING']
                        transition_message = "Great, thank you for providing that information. Now, based on your tech stack, here are a few technical questions for you:"
                        st.session_state.messages.append({"role": "assistant", "content": transition_message})
                        st.markdown(transition_message)
                        
                        question_prompt = prompts.QUESTION_GENERATION_PROMPT_TEMPLATE.format(
                            tech_stack=get_chat_history_string()
                        )
                        tech_questions = get_llm_response(question_prompt)
                        if tech_questions:
                            st.session_state.messages.append({"role": "assistant", "content": tech_questions})
                            st.markdown(tech_questions)
                        else:
                            st.error("Could not generate technical questions.")
                    else:
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.markdown(response)

    elif st.session_state.stage == CONVERSATION_STAGES['QUESTIONING']:
        st.session_state.stage = CONVERSATION_STAGES['CLOSING']
        closing_message = prompts.CLOSING_MESSAGE
        st.session_state.messages.append({"role": "assistant", "content": closing_message})
        with st.chat_message("assistant"):
            st.markdown(closing_message)