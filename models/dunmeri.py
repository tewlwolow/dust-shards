from models.blueprint import Language

class AldDunmeri(Language):
    def __init__(self):
        data = 'data/ald.toml'
        super().__init__(data)

class YanDunmeri(Language):
    def __init__(self):
        data = 'data/yan.toml'
        super().__init__(data)
