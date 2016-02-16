import logging
from bot import MyBot
import settings

from requests.exceptions import ReadTimeout

if __name__ == "__main__":
    # On set le logging
    logging.basicConfig(format='%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s', level=logging.INFO)
    # On créé l'objet bot avec la config passée dans le fichier settings (depuis l'import settings)
    bot = MyBot(settings.CHAN, settings.NICKNAME, settings.SERVER, settings.PORT)

    while True:
        try:
            logging.info('Demarrage de la surveillance de masse')
            bot.start()
        except ReadTimeout:
            logging.error('Read timeout, restarting bot.')
