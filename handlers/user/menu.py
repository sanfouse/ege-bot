from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.user.keyboard import (check_question_keyboard,
                                     check_questions_keyboard_false,
                                     check_questions_keyboard_true,
                                     numbers_menu_keyboard,
                                     start_menu_keyboard)
from loader import dp
from states.user.distribution import *
from utils.db.manager_database import Questions, User

from .text import START_MESSAGE


async def check_start(user_id, username):
  data = await User.query.where(User.id==user_id).gino.scalar()

  nickname = 'noname'

  if username is not None:
    nickname = username

  if data is None:
    await User.create(
      id=user_id,
      nickname=nickname
    )

@dp.message_handler(commands='start')
async def start(message: types.Message):
  await check_start(
    user_id=message.from_user.id,
    username=message.from_user.username
  )

  await message.answer(
    f'Hello, {message.from_user.full_name}', reply_markup=start_menu_keyboard()
  )

  await message.answer(
    START_MESSAGE, reply_markup=numbers_menu_keyboard()
  )
  await CheckNumbers.menu.set()



@dp.message_handler(lambda m: m.text == 'Обо мне', state=CheckNumbers.menu)
async def start_numbers(message: types.Message):
  user = await User.query.where(User.id==int(message.from_user.id)).gino.first()
  await message.answer(user)


@dp.callback_query_handler(lambda c: c.data.split(' ')[0] == 'menu', state=CheckNumbers)
async def menu(call: types.CallbackQuery, state: FSMContext):
  await CheckNumbers.menu.set()
  data = await state.get_data()
  await state.update_data(
      {
        call.data.split(' ')[1]: int(data[call.data.split(' ')[1]])
      }
    )
  await call.message.answer(
    f'Выберите номер: ', reply_markup=start_menu_keyboard()
  )
  await call.message.edit_text(
    START_MESSAGE, reply_markup=numbers_menu_keyboard()
  )


@dp.callback_query_handler(lambda c: c.data.isdigit(),state=CheckNumbers.menu)
async def get_questions(call: types.CallbackQuery, state: FSMContext):
  data = await state.get_data()
  if not data:
    await state.update_data(
      {
        call.data: 0
      }
    )
  if call.data not in data:
    await state.update_data(
      {
        call.data: 0
      }
    )

  question = await Questions.query.where(Questions.ege_number==int(call.data)).gino.all()
  data = await state.get_data()
  
  await state.update_data(
    {
      call.data: int(data[call.data]),
      'question': question[int(data[call.data])]
    }
  )

  await User.update.values(questions=User.questions + 1).where(User.id==int(call.from_user.id)).gino.status()
  await CheckNumbers.check_answer.set()
  await call.message.edit_text(text=question[int(data[call.data])], reply_markup=check_question_keyboard(call.data))
  await call.message.answer(text='Введите ответ:', reply_markup=types.ReplyKeyboardRemove(True))


@dp.message_handler(state=CheckNumbers.check_answer)
async def check_responce(message: types.Message, state: FSMContext):
  data = await state.get_data()
  question = data.get('question')
  questions = await Questions.query.where(Questions.ege_number==int(str(question.ege_number))).gino.all()

  true_answers = question.answer.split(' ')[1]
  true_answers = true_answers.split('|')
 
  if message.text.lower() in true_answers:
      await CheckNumbers.menu.set()
      await message.answer(text='Молодец! Ты ответил правильно', reply_markup=check_questions_keyboard_true(
            number=question.ege_number, url=question.url
          )
        )
      await state.update_data(
          {
            str(question.ege_number): int(data[str(question.ege_number)]) + 1,
            'question': questions[int(data[str(question.ege_number)]) + 1]
          }
        )
      await User.update.values(correct_answers=User.correct_answers + 1).where(User.id==int(message.from_user.id)).gino.status()

  else:
    await message.answer('Неверно, попробуйте снова', reply_markup=check_questions_keyboard_false(
          question.ege_number, question.url)
        )