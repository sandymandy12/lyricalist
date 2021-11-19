from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from Lyrics import Lyrics
from Speech import Speech


def newBrowser(headless=True):
    service = Service('/opt/homebrew/bin/geckodriver')
    options = Options()
    options.page_load_strategy = 'normal'
    if headless is True:
        options.add_argument("--headless")

    return webdriver.Firefox(
        service=service,
        options=options
    )


lyrics = Lyrics(newBrowser(headless=True))
speech = Speech(newBrowser(headless=False))

lyrics.generate()
lyrics.write_to_file()

link = speech.generate(lyrics.text_to_speech())
speech.write_to_file()
