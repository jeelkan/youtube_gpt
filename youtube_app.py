import pandas as pd
import numpy as np
import streamlit as st
import whisper
import pytube
from pytube import YouTube
from streamlit_chat import message
import openai
import os
#import pinecone
from dotenv import load_dotenv
from scipy.spatial.distance import cosine


# whisper
model = whisper.load_model('base')
output = ''
data = []
data_transcription = []
embeddings = []
mp4_video = ''
audio_file = ''

# Pinacone

# Uncomment this section if you want to save the embedding in pinecone
#load_dotenv()
# initialize connection to pinecone (get API key at app.pinecone.io)
# pinecone.init(
#     api_key=os.getenv("PINACONE_API_KEY"),
#     environment=os.getenv("PINACONE_ENVIRONMENT")
# )
array = []

# Uncomment this section if you want to upload your own video
#Sidebar
with st.sidebar:
    user_secret = st.text_input(label = ":red[OpenAI API key]",
                                value="",
                                placeholder = "Paste your openAI API key, sk-",
                                type = "password",
                                key="openai_api_key")
    youtube_link = st.text_input(label = ":red[Youtube link]",
                                value="https://youtu.be/rQeXGvFAJDQ",
                                placeholder = "",
                                key="youtube_link")
    if youtube_link and user_secret:
        youtube_video = YouTube(youtube_link)
        video_id = pytube.extract.video_id(youtube_link)
        streams = youtube_video.streams.filter(only_audio=True)
        stream = streams.first()
        if st.button("Start Analysis"):
            if os.path.exists("word_embeddings.csv"):
                os.remove("word_embeddings.csv")
                
            with st.spinner('Running process...'):
                # Get the video mp4
                mp4_video = stream.download(filename='youtube_video.mp4')
                audio_file = open(mp4_video, 'rb')
                st.write(youtube_video.title)
                st.video(youtube_link) 

                # Whisper
                output = model.transcribe("youtube_video.mp4")
                
                # Transcription
                transcription = {
                    "title": youtube_video.title.strip(),
                    "transcription": output['text']
                }
                data_transcription.append(transcription)
                pd.DataFrame(data_transcription).to_csv('transcription.csv') 
                segments = output['segments']

                os.remove("youtube_video.mp4")
                st.success('Analysis completed')

st.markdown('<h1><center>Youtube GPT 🤖</center></h1>', unsafe_allow_html=True)
#st.write("Start a chat with this video of Microsoft CEO Satya Nadella's interview. You just need to add your OpenAI API Key and paste it in the 'Chat with the video' tab.")

DEFAULT_WIDTH = 80
VIDEO_DATA = "https://youtu.be/bsFXgfbj8Bc"

width = 40

width = max(width, 0.01)
side = max((100 - width) / 2, 0.01)

_, container, _ = st.columns([side, 47, side])
container.video(data=VIDEO_DATA)
tab1, tab2, tab3 = st.tabs(["Intro", "Transcription", "Chat with the Video"])
with tab1:
    st.markdown("### How does it work?")
    #st.markdown('Read the article to know how it works: [Medium Article]("https://medium.com/@dan.avila7/youtube-gpt-start-a-chat-with-a-video-efe92a499e60")')
    st.write("Youtube GPT was written with the following tools:")
    st.markdown("#### Code GPT")
    st.write("All code was written with the help of Code GPT. Visit [codegpt.co](https://codegpt.co) to get the extension.")
    st.markdown("#### Streamlit")
    st.write("The design was written with [Streamlit](https://streamlit.io/).")
    st.markdown("#### Whisper")
    st.write('Video transcription is done by [OpenAI Whisper](https://openai.com/blog/whisper/).')
    #st.markdown("#### Embedding")
    #st.write('[Embedding]("https://platform.openai.com/docs/guides/embeddings") is done via the OpenAI API with "text-embedding-ada-002"')
    st.markdown("#### GPT-3")
    st.write('The chat uses the OpenAI API with the [GPT-3](https://platform.openai.com/docs/models/gpt-3) model "gpt-3.5-turbo""')
    st.markdown("""---""")
    st.write('Author: [Jeel Kanzaria](https://www.linkedin.com/in/jeel-kanzaria/)')
    st.write('Repo: [Github](https://github.com/jeelkan/youtube_gpt)')
    st.write("This software was developed with Code GPT, for more information visit: https://codegpt.co")
with tab2: 
    st.header("Transcription:")
    if os.path.exists("youtube_video.mp4"):
        audio_file = open('youtube_video.mp4', 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')
        audio_file.close()  # It's important to close the file after reading

    if os.path.exists("transcription.csv"):
        df = pd.read_csv('transcription.csv')
        st.write(df)

# Function to handle chat-based interaction with OpenAI's GPT-3.5-turbo
def generate_chat_response(api_key, messages):
    openai.api_key = api_key
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']


with tab3:
    user_secret = st.text_input(label=":blue[OpenAI API key]",
                                placeholder="Paste your OpenAI API key, sk-",
                                type="password")
    
    st.write('To obtain an API Key you must create an OpenAI account at the following link: https://openai.com/api/')
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("Ask me something about the video:", key="input")
    
    if user_input:
        if os.path.exists('transcription.csv'):
            df_transcription = pd.read_csv('transcription.csv')
            combined_transcriptions = " ".join(df_transcription['transcription'].astype(str).tolist())
            
            chat_messages = [{
                'role': 'system',
                'content': f"Transcription:\n{combined_transcriptions}"
            }] + [{'role': 'user', 'content': user_input}] + st.session_state.chat_history
            
            response_content = generate_chat_response(user_secret, chat_messages)
            
            # Update chat history
            st.session_state.chat_history.append({'role': 'assistant', 'content': response_content})
            
            # Display conversation
            for message in reversed(st.session_state.chat_history):
                role = "You" if message['role'] == 'user' else "Assistant"
                st.text_area("", value=f"{role}: {message['content']}", height=300, disabled=True)
        else:
            st.error("Transcription data not found. Please ensure the transcription process is completed successfully.")


    
