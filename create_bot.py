from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# TOKEN = '5663487719:AAH1nCz5zYQrMww-epWRWo4CP_Op9YaBGbg'
# TOKEN = '5636707541:AAGGy6KEvEShuPl9k-PctHWlw2hphdy6rdw'
# TOKEN = '5845355889:AAEWSRG9LXkWTaIad_hCwOLTrj1I6ZUy5Ak'
TOKEN = '5854421058:AAF4YYOs3kjdjFVIo7OUkfWf59lMw_h7l9A'

# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
