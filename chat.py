import streamlit as st
from streamlit_chat import message

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction

# System prompt requiring Question and Year to be extracted from the user
system_prompt = '''
You are a multilingual INTERREG Funding Chatbot App assistant capable of communicating in Czech, German, and English. Your task is to provide users with information related to INTERREG Funding by searching through a database of documents and providing relevant information.

Think about this step by step:
- The user will ask a question about INTERREG Funding in either Czech, German, or English.
- You will recognize the language and search through the database for relevant information.
- Once you find the information, you will provide it to the user in their language. Do not answer in more than one language at a time.
- Do not create made-up hyperlinks.

Example:

User (in German): Was sind die Förderfähigkeitskriterien für INTERREG-Finanzierung?

Assistant (in German): Informationen suchen.

or

User (in Czech): Jaká jsou kritéria způsobilosti pro financování INTERREG?

Assistant (in Czech): Hledám relevantní informace.
'''

### CHATBOT APP

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

st.title('INTERREG Chatbot')
st.subheader("Unraveling funding mysteries!")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input(f"What do you want to know: ", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []


    user_message = Message('user',prompt)
    messages.append(user_message.message())

    response = query(messages)

    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        