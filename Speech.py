from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import random


class Speech():

    def __init__(self, driver):
        self.driver = driver
        self.link = ''

    def generate(self, tts):
        self.tts = tts

        print("\nLoading speech webpage...\n")
        self.driver.get('https://spik.ai/')
        url = self.driver.current_url

        text_box = self.driver.find_element(By.NAME, "text_to_generate")
        text_box.clear()

        [text_box.send_keys(line) for line in tts]

        voice_element = Select(
            self.driver.find_element(By.ID, 'id_voice_type'))
        option = random.randrange(len(voice_element.options))

        voice_opt = voice_element.options[option]
        voice_opt.click()
        voice = voice_opt.get_attribute('innerText')
        print("Selected Voice:", voice)

        print("\nGenerating Voice...\n")
        self.driver.find_element(
            By.CSS_SELECTOR, '#voice_generate_form > div > button'
        ).click()

        try:
            WebDriverWait(self.driver, 20).until(EC.url_changes(url))
            self.link = self.driver.current_url
        except TimeoutException:
            print("Timed out waiting for url to change")

        print('Link: ', self.link)

        self.driver.quit()
        return self.link

    def download(self, link):
        driver = self.driver
        driver.get(link)

        driver.quit()

    def write_to_file(self, link_file="links.txt"):
        print('writing to LINKS file..')
        f = open(link_file, 'a')
        f.write(self.link)
        f.close()
        # with open(link_file, 'wb') as f:
        #     try:  # catch OSError in case of a one line file
        #         f.seek(-2, os.SEEK_END)
        #         while f.read(1) != b'\n':
        #             f.seek(-2, os.SEEK_CUR)
        #     except OSError:
        #         f.seek(0)
        #     last_line = f.readline().decode()
        #     if len(last_line.split(',')) > 5:
        #         f.write(f'\n{self.link}, ')
        #     else:
        #         f.write(f'{self.link}, ')
