from PyPDF2 import PdfFileReader
from google.cloud import texttospeech
from google.cloud import storage
import pyglet
from time import sleep


# this will look at the pdf file and start to extract some small bits to read, you can modify this as needed
def extract_information(path_to_pdf_file):
    with open(path_to_pdf_file, 'rb') as file:
        pdf = PdfFileReader(file)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of Pages: {number_of_pages}"""

    # return information to be saved into a variable to send to Google Text to Speech API
    return txt


# convert the text extracted from pdf file
def convert_to_speech(text):

    # create a client with google cloud and send credentials via json file
    client = texttospeech.TextToSpeechClient.from_service_account_json('TTSKey.json')

    input_text = texttospeech.SynthesisInput(text=text)

    # these are optional params and can be modified or left for google to decide
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # this can be in .wav or mp3 as needed per the google docs
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    # this will save your converted text into a separate file
    with open("output.mp3", "wb") as output_mp3_from_pdf:
        output_mp3_from_pdf.write(response.audio_content)


# this part is optional if you want to let the newly saved file autoplay using the pyglet library
def play_extracted_text(file_name):

    music = pyglet.media.load(filename=file_name, streaming=False)
    music.play()

    # this is needed to make sure the file will play entirely before the script ends
    sleep(music.duration)


if __name__ == '__main__':

    path = 'C:/Users/wtpar/PycharmProjects/pdf_to_speechprogram/reportlab-sample.pdf'
    info = extract_information(path)
    print(info)  # just to make it easier to confirm the extracted data matches what the google api creates
    convert_to_speech(info)
    play_extracted_text('output.mp3')


