import re
import pyphen
dic = pyphen.Pyphen(filename='data/ald.dic')

CONSONANTS = r'([^aeiou]+)'
CLUSTERS = r'([qwrtypsdfghjklzxcvbnm]{1,4})'
DOUBLES = r'(\w)\1'

class WordParser:

    def __init__(self, word):

        def get_syllables() -> list:
            return dic.inserted(self.word.lower().replace('-', '')).split('-')

        def get_stems():
            stems = []
            for syllable in self.syllables:
                consonants = ''.join(re.findall(CONSONANTS, syllable))
                stems += re.findall(CLUSTERS, consonants)
            return stems

        self.word = word
        self.syllables = get_syllables()
        self.stems = get_stems()
