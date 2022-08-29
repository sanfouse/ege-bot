import asyncio

from gino import Gino
from utils.config import DATABASE_URL

db = Gino()


class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer(), primary_key=True)
  nickname = db.Column(db.Unicode(), default='noname')

  questions = db.Column(db.Integer(), default=0)
  correct_answers = db.Column(db.Integer(), default=0)

  def __repr__(self):
    return f"""
<b>ID:</b> {self.id}   
<b>USERNAME:</b> {self.nickname}
<b>Вопросов:</b> {self.questions}
<b>Верно отвеченных</b> {self.correct_answers}
"""


class Questions(db.Model):

  __tablename__ = 'questions'

  id = db.Column(db.Integer(), primary_key=True)
  ege_number = db.Column(db.Integer())
  url = db.Column(db.String())

  questions = db.Column(db.String())
  answer = db.Column(db.String)

  def __repr__(self): 
    return f"""
Id: {self.id}
Номер ЕГЭ: {self.ege_number} 
<i>{self.questions}</i>
"""


async def main():
  await db.set_bind(
    DATABASE_URL
  )
  print('[*] >> DATABASE CONNECTED')
  await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(main())