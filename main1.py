import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Your goal is to:
    - Find canabis strain that will help with pain based on simptoms and desired effects

    Here are some examples different Pains:
    - Acute: Acute pain happens quickly and goes away when there is no cause.
    - Chronic Pain: Lasts longer than six months and can continue when the injury or illness has been treated.  

    Here are some examples of words in different effects:
    - Indica: Relaxed, hungry, sleepy.
    - Sativa: energetic, creative, focused
    

    Please start the recommendation with a warm introduction.
    
    Below is the pain, effects, and simptoms:
    # PAIN: {pain} 
    # EFFECTS: {effects}
    # SIMPTOMS: {simptoms}
    
    YOUR RESPONSE:
"""


prompt = PromptTemplate(
    input_variables=["pain", "effects", "simptoms"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Strains4pain", page_icon=":robot:")
st.header("Strains for Pain")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Cannabinoids, such as tetrahydrocannabinol (THC) and cannabidiol (CBD), are found in cannabis. \n\n CBD can help\
                 reduce chronic inflammation and pain. CBD also affects opioid receptors. Opioid receptors are important in \
                regulating pain; this is why opioids are prescribed for chronic pain treatment. CBD binds to opioid receptors and alters \
                how they respond to stimuli, ultimately reducing pain.This tool \
                will help you improve your pain by recommending best Canabbis strains for pain. This tool \
                is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
                [@myzona](https://github.com/myzona). \n\n View Source Code on [Github](https://github.com/myzona/strains4pain1)") 

with col2:
    st.image(image='img_strain1.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter Your Simptoms")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which pain you have?',
        ('Acute', 'Chronic Pain'))
    
with col2:
    option_dialect = st.selectbox(
        'Which Effects would you like?',
        ('Sativa', 'Indica'))

def get_text():
    input_text = st.text_area(label="Input", label_visibility='collapsed', placeholder="Your Simptoms...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "I can't sleep and I have a headache. I would like to feel relaxed and sleepy."

st.button("*Tell me*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Recommendations:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(pain=option_tone, effects=option_dialect, simptoms=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)