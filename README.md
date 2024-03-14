
# YouTube GPT 🤖

YouTube GPT is a cutting-edge application that brings the power of AI-driven conversation to YouTube videos. It allows users to interact with video content in a novel way by asking questions and receiving answers based on the video's transcription. Utilizing OpenAI's Whisper for accurate transcriptions and GPT-3 for generating conversational responses, YouTube GPT offers a unique way to engage with video content.

## How It Works

1. **Transcription**: The application first downloads the audio from a specified YouTube video and uses OpenAI Whisper to generate a text transcription.
2. **Interaction**: Users can then ask questions related to the video's content. The application uses GPT-3.5-turbo to understand the question within the context of the transcription and generate relevant answers.
3. **Insights**: Beyond simple Q&A, YouTube GPT can summarize the video, offering quick insights and takeaways without watching the entire content.

## Built With

- [Streamlit](https://streamlit.io/) - The fastest way to build and share data apps.
- [OpenAI Whisper](https://openai.com/blog/whisper/) - Robust speech recognition model for transcription.
- [OpenAI GPT-3](https://openai.com/api/) - State-of-the-art language processing AI model for generating conversational responses.
- [PyTube](https://pytube.io/en/latest/) - A lightweight, dependency-free Python library (and command-line utility) for downloading YouTube Videos.

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API Key
- Streamlit

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username_/youtube_gpt.git
   ```
2. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```sh
   streamlit run youtube_app.py
   ```

## Usage

1. **Enter your OpenAI API key**: Securely input your key to enable transcription and conversation capabilities.
2. **Paste a YouTube link**: Specify the video you want to interact with.
3. **Ask Questions**: Navigate to the "Chat with the Video" tab and start asking questions related to the video content.

## Authors

- **Jeel Kanzaria** - *Initial work* - [JeelKanzaria](https://linkedin.com/in/jeel-kanzaria)

## Acknowledgments

- This software was developed with the help of Code GPT. For more information, visit [codegpt.co](https://codegpt.co).
- Special thanks to the OpenAI team for providing the tools that power this application.

---

Feel free to customize the README further to match your project's needs or to add additional sections such as screenshots, contributing guidelines, license information, etc.
