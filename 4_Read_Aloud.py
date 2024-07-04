import streamlit as st
import os
import time
import glob
from gtts import gTTS
from deep_translator import GoogleTranslator

# Create a temporary directory if it doesn't exist
if not os.path.exists("temp"):
    os.mkdir("temp")

st.set_page_config(
    page_title="Read Aloud",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header("Read Aloud", divider="grey", anchor=False)

text = st.text_input("Enter text")

in_lang = st.selectbox(
    "Select your input language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
)

input_language = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}[in_lang]

out_lang = st.selectbox(
    "Select your output language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese")
)

output_language = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Japanese": "ja"
}[out_lang]

english_accent = st.selectbox(
    "Select your English accent",
    (
        "Default", "India", "United Kingdom", "United States",
        "Canada", "Australia", "Ireland", "South Africa"
    )
)

tld = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za"
}[english_accent]

def text_to_speech(input_language, output_language, text, tld):
    try:
        translation = GoogleTranslator(source=input_language, target=output_language).translate(text)
        tts = gTTS(translation, lang=output_language, tld=tld, slow=False)
        my_file_name = text[:20] if len(text) > 0 else "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, translation
    except Exception as e:
        return None, f"Translation failed: {str(e)}"

display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    if result:
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## Output text:")
            st.write(output_text)
    else:
        st.error("Error: " + output_text)

def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
            print("Deleted ", f)

remove_files(7)
