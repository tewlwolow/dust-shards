from languages.dunmeri import AldDunmeri
ald_dunmeri = AldDunmeri()

import sys
from ui.app import DustShards

if __name__ == '__main__':
    app = DustShards(sys.argv)
    sys.exit(app.exec())