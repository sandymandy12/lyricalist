import requests
import re
import random


def random_word():
    word_type = random.choice(['noun', 'adjective', 'animal'])
    response = requests.get(
        # 'https://random-word-api.herokuapp.com/word?number=1'
        f'https://random-word-form.herokuapp.com/random/{word_type}?count=1'
    )
    word = response.content.decode('utf')
    return re.sub(r'[\W_]+', '', word)


# print(random_word())
