import models.dunmeri as dunmeri
class Languages:
    archive = None

    def __init__(self):
        self.archive: list = [dunmeri.AldDunmeri()]