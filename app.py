import pytube
import requests
import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from bardapi import Bard
from dotenv import find_dotenv, load_dotenv
import openai

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
BARD_API_KEY=os.getenv("BARD_API_KEY")
bard = Bard(token=BARD_API_KEY)

# Extract audio from YouTube
def get_audio(video_url):
    print("-----GETTING AUDIO-----")
    # Create a PyTube object for the video.
    youtube_video = pytube.YouTube(video_url)

    # Get the audio stream from the video.
    audio_stream = youtube_video.streams.filter(only_audio=True)

    # Download the audio stream to a file.
    audio_stream[0].download(output_path="audios", filename="audio.mp3")
    print("-----GETTING AUDIO DONE-----")

# Audio to text
def get_text(filename):
    print("-----GENERATING TRANSCRIPT-----")
    audio_file= open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print("-----TRANSCRIPT GENERATED-----")
    return transcript

def get_facts(transcript):
    print("-----EXTRACTING FACTS-----")

    template = """
    Given this text. Extract top ten facts from it.;

    CONTEXT: {transcript}
    FACTS:
    """

    prompt = PromptTemplate(template=template, input_variables=["transcript"])

    fact_llm = LLMChain(llm=ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=1), prompt=prompt, verbose=True)
    
    facts = fact_llm.predict(transcript=transcript)

    print("Here are the facts", facts)

    return facts

def organize_facts(facts):
    # Split the input text into individual facts based on a delimiter
    facts_text = facts.split("\n")

    organized_facts = []

    for i, fact_text in enumerate(facts_text, start=1):
        organized_fact = {
            "description": fact_text.strip()  # Remove leading/trailing whitespaces
        }
        organized_facts.append(organized_fact)

    return organized_facts

def check_facts(organized_facts):
    print("-----CHECKING FACTS NOW-----")
    for fact in organized_facts:
        # print(f"{fact['description']}")
        fact_to_check = fact['description']
        query = f"""
        Answer in yes or no. Check if the following statement is factually correct. Check years, names, locations, historical events, numbers, or any other named entity. {fact_to_check} ?
        Also cite sources for your answer by mentioning URLs.
        """
        answer = bard.get_answer(query)['content']
        print(fact)
        print (answer)
        print("------")


get_audio("https://www.youtube.com/watch?v=KaWihejcGcM")
transcription = get_text("audios/audio.mp3")
facts = get_facts(transcription)
organized_facts = organize_facts(facts)
check_facts(organized_facts)