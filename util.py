import re
import pyphen
dic = pyphen.Pyphen(filename='data/ald.dic')

CONSONANTS = r'([^aeiou]+)'
CLUSTERS = r'([qwrtypsdfghjklzxcvbnm]{1,4})'
DOUBLES = r'(\w)\1'

def syllabise(word: str) -> list:
    hyphenated = dic.inserted(word)
    return hyphenated.split('-')

def get_stem(word: str):
    stems = []
    syllabised = syllabise(word.lower())
    for syllable in syllabised:
        consonants = ''.join(re.findall(CONSONANTS, syllable))
        stems += re.findall(CLUSTERS, consonants)
        print("\n")
    return stems
