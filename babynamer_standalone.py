from traceback import TracebackException
import streamlit as st
import datetime
from app.utilities.gpt3complete import gpt3complete, presets_parser
from flask_sqlalchemy import SQLAlchemy
st.set_page_config(page_title='WebBabyShower.com', page_icon = "https://webbabyshower.com/wp-content/uploads/2017/12/cropped-WBS-logo-Yellow-300px-32x32.png", layout = 'wide', initial_sidebar_state = 'auto')

def post_process_text(text):
    #all_patterns = [r'<br\s*?>', r'<br>', r'<li>', r'\n\s*\n', r'^-\s+', r'^-', r'\d+[)]'
    #combined_patterns =  = r'|'.join(map(r'(?:{})'.format, all_pats))
    text = text.replace('<br\s*?>', '')
    text = text.replace('<br>', '\n')
    text = text.replace('<li>', '\n')
    text = re.sub(r'\d+[)]', "", text)
    text = text.replace('\n-', '\n')
    text = text.replace('\n• ','\n')
    text = text.replace('\n ', '\n')
    text = re.sub('[\n]+', '\n', text)
    text = re.sub('\d+[.]\s+', '', text).rstrip()
    text = re.sub('\d+[.\n]\s+', '', text).rstrip()
    text = text.replace('\\n', '\n')
    text = re.sub('[\n]+', '\n', text)
    text = text.replace('###', '\n\n')
    print('post processed text is', '\n' + text)
    return text


def preset2streamlit(preset):
    presetdf = presets_parser(preset)[0]
    #st.write(presetdf.astype(str).transpose())
    #st.write(preset)
    label = presetdf['preset_name'].iloc[0]
    prompt = presetdf['prompt'].iloc[0]
    #st.write(prompt)
    if not prompt:
        prompt = ''
    with st.form(key=preset, clear_on_submit=False):
        if presetdf['preset_pagetype'].iloc[0]  == 'NoUserInput':
            st.markdown(presetdf['preset_instructions'].iloc[0])
            st.form_submit_button(label="Make a Baby (Name)") 
            response = gpt3complete(preset, prompt) # prompt is predefined by preset
            #st.write(response)
            #response_text = response['choices'][0]['text']
            response_text = post_process_text(response['choices'][0]['text'])
            completion_heading = f"##### {presetdf['completion_heading'].iloc[0]}"
            st.markdown(completion_heading)
            st.markdown(response_text)
            #st.text(response_text)
            st.markdown("""Return to [WebBabyShower.com](https://webbabyshower.com) to plan the shower, the gender reveal, and more.""")

        elif presetdf['preset_pagetype'].iloc[0] == "UserPrompt":

            prompt = st.text_input(label, key=preset,value=presetdf['preset_placeholder'].iloc[0],max_chars=100, autocomplete="on")
            st.markdown(presetdf['preset_instructions'].iloc[0])
            st.form_submit_button(label="Generate")
            response = gpt3complete(preset, prompt)
            response_text = response['choices'][0]['text']
            completion_heading = f"##### {presetdf['completion_heading'].iloc[0]}"
            st.markdown(completion_heading)
            st.write(response_text)

        elif presetdf['preset_pagetype'].iloc[0] == "UserTextArea":
            prompt = st.text_area(label, key=preset,value=presetdf['preset_placeholder'].iloc[0],max_chars=100)
            st.markdown(presetdf['preset_instructions'].iloc[0])
            st.form_submit_button(label="Generate")
            response = gpt3complete(preset, prompt)
            response_text = response['choices'][0]['text']
            completion_heading = f"##### {presetdf['completion_heading'].iloc[0]}"
            st.markdown(completion_heading)
            st.write(response_text)
        else:
            Exception("Page type not recognized")
            st.write(Exception)
        return 

with st.expander('Easiest option!', expanded = True):
    preset2streamlit('baby-name-no-user-input-function')
with st.expander("Request particular types of names",):
    preset2streamlit('baby-name-generator')
