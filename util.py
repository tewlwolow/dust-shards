import re

CONSONANTS = r'([^aeiou]+)'
CLUSTERS = r'([qwrtypsdfghjklzxcvbnm]{2,4})'
STEMS = r'(nm|bnb|ddm)'

class Util:
    def __init__(self):
        pass

    @staticmethod
    # def get_stem(word: str):
    #     consonants = ''.join(re.findall(CONSONANTS, word.lower()))
    #     clusters = ''.join(re.findall(CLUSTERS, consonants))
    #     return re.findall(STEMS, clusters)

    def get_stem(word: str):
        consonants = ''.join(re.findall(CONSONANTS, word.lower()))
        return re.findall(CLUSTERS, consonants)
