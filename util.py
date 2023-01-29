import re

PATTERN = r'([^aeiou]+)'

class Util:
    def __init__(self):
        pass

    @staticmethod
    def get_stem(word: str):
        return re.findall(PATTERN, word.lower())
