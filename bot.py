from aiogram import executor
from loader import dp



if __name__ == '__main__':
  import handlers
  import utils.db.manager_database
  executor.start_polling(dp)