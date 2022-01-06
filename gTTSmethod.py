from PyPDF2 import PdfFileReader
from gtts import gTTS
from tempfile import TemporaryFile
from time import sleep
import pyglet
import os


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

    # return information
    return txt


if __name__ == '__main__':
    path = 'C:/Users/wtpar/PycharmProjects/pdf_to_speechprogram/reportlab-sample.pdf'

    info = extract_information(path)
    print(info)

    # gTTS is a library that you can import to use if you don't want to use the google api
    tts = gTTS(text=info, lang='en')
    tts.save('pdf_example.mp3')

    # this will let the music play after it has been created
    music = pyglet.media.load(filename="pdf_example.mp3", streaming=False)
    music.play()
    sleep(music.duration)
    # if you want to remove the file after it plays
    # os.remove('pdf_example.mp3')
