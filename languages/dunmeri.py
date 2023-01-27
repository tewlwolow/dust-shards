from languages.blueprint import Language

class AldDunmeri(Language):
    def __init__(self):
        data = 'data/ald.toml'
        super().__init__(data)