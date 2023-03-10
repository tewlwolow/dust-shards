import tomllib

class Language:
    """
    A base class for all models in our project.
    """
    def __init__(self, data):
        with open(data, mode='rb') as metadata:
            self.data = tomllib.load(metadata)

        self.name = self.data['name']
        self.description = self.data['description']
        self.history = self.data['history']
        self.corpus = {'vanilla': self.data['corpus']['vanilla']}

