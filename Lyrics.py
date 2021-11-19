from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchAttributeException
from selenium.webdriver.support import expected_conditions as ec
from Utils import random_word
import random
import datetime


class Lyrics():

    def __init__(self, driver):
        self.topic_value = random_word()
        self.driver = driver
        self.errors = 0

    def generate(self, recalled=False):
        print("\nLoading lyrics webpage...")
        if recalled:
            self.driver.delete_all_cookies()
            self.driver.refresh()
            self.topic_value = random_word()
        else:
            self.driver.get('https://theselyricsdonotexist.com/')

        #  set genre
        self.g = random.choice(
            ['country', 'metal', 'rock', 'pop', 'rap', 'edm']
        )
        #  set mood
        self.m = random.choice(
            ['verysad', 'sad', 'neutral', 'happy', 'veryhappy']
        )

        topic = self.driver.find_element(By.ID, "generateInputSeed")
        genre = self.driver.find_element(
            By.CLASS_NAME, f'mini-button-{self.g}')
        mood = self.driver.find_element(By.CLASS_NAME, f'mini-button-{self.m}')

        topic.clear()
        topic.send_keys(self.topic_value)
        genre.click()
        mood.click()

        print("Selected Topic:", self.topic_value)
        print("Selected Genre:", self.g)
        print("Selected Mood:", self.m)

        print("\nGenerating lyrics...\n")
        self.driver.find_element(
            By.ID, 'generateButton').click()  # generates lyics

        innerText = ''
        try:
            popup = self.driver.find_element(By.ID, 'dialogMessage')
            innerText = str(popup.get_attribute('innerText')).strip()
            if len(innerText) > 0:
                raise NoSuchAttributeException(innerText)

            element = WebDriverWait(self.driver, 5, poll_frequency=1).until(
                ec.visibility_of_element_located(
                    (By.ID, 'generateLyricsView')
                )
            )
            self.lyrics = element.get_attribute('innerText')

        except TimeoutException:
            print("timed out..")
            return self.generate(True)
        except NoSuchAttributeException as e:
            print(e.msg)
            self.errors += 1
            if self.errors < 10:
                return self.generate(True)
            else:
                print('too many errors')
        except Exception as e:
            print('separate error now')
            print(e)

        print('done generating!')
        self.driver.quit()

    def text_to_speech(self):
        obj = []
        for line in self.lyrics.split('\n' * 2):
            l = line.split('\n')
            [obj.append(l[x]) for x in range(1, len(l))]

        print("Text to speech:\n", obj)
        return obj

    def write_to_file(self, notes='', lyrics='', lyric_file="lyrics.txt"):

        print('writing to lyrics file..')
        lyric = self.lyrics if lyrics == '' else lyrics
        f = open(lyric_file, 'a')
        f.write(
            f'\n~~~~~~~~ {self.topic_value} | {self.m} | {self.g} ~~~~~~~\n'
        )
        if notes != '':
            f.write(f'~~~ {notes} ~~~\n')

        f.write(lyric)
        f.write(f'\n~~~~~~~~ {datetime.datetime.now()} ~~~~~~~\n\n')
        f.close()

    def speech_link(self, driver):
        print("\nLoading speech webpage...\n")
        self.driver = driver
        self.driver.get('https://spik.ai/')
        url = self.driver.current_url

        tts = self.text_to_speech()

        # text_box = self.driver.find_element(By.NAME, "text_to_generate")
        # text_box.clear()

        # [text_box.send_keys(line) for line in tts]

        # voice_element = Select(driver.find_element(By.ID, 'id_voice_type'))
        # option = random.randrange(len(voice_element.options))

        # voice_opt = voice_element.options[option]
        # voice_opt.click()
        # voice = voice_opt.get_attribute('innerText')
        # print("Selected Voice:", voice)

        # print("\nGenerating Voice...\n")
        # self.driver.find_element(
        #     By.CSS_SELECTOR, '#voice_generate_form > div > button'
        # ).click()

        # try:
        #     WebDriverWait(self.driver, 20).until(EC.url_changes(url))
        #     self.link = self.driver.current_url
        # except TimeoutException:
        #     print("Timed out waiting for url to change")

        # print(self.link)

        self.driver.quit()
