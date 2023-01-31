import re

BASIC = r'([^aeiou]+)'
GROUPING = r'([qwrtypsdfghjklzxcvbnm]{2,4})'

class Util:
    def __init__(self):
        pass

    @staticmethod
    def get_stem(word: str):
        stems = ''.join(re.findall(BASIC, word.lower()))
        return re.findall(GROUPING, stems)
