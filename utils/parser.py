import asyncio

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from db.manager_database import Questions


class EgeNumbers:

    def _load_page(self, url):
        wd = webdriver.Chrome(service=Service('./driver/chromedriver'))
        wd.get(url)
        return wd.page_source

    def get_questions(self):
        html = self._load_page('https://rus-ege.sdamgia.ru')
        links = self._get_links(html)
        asyncio.get_event_loop().run_until_complete(self._get_questions(links))

    def _get_links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        data = []
        links = soup.find_all('a', class_='Link Link_black')
        for link in links:
            link = 'https://rus-ege.sdamgia.ru' + link.get('href') + '&print=true'
            data.append(link)
        return data

    async def _get_questions(self, links):
        for link in links:
            html = self._load_page(link)
            soup = BeautifulSoup(html, 'lxml')
            questions = soup.find_all('div', class_='prob_maindiv')
            for question in questions:
                prob_nums = question.find('span', class_='prob_nums')
                url = 'https://rus-ege.sdamgia.ru' + prob_nums.find('a').get('href')
                answer = question.find('div', class_='answer').text
                question = question.find('div', class_='nobreak').text
                ege_number = int(prob_nums.text.split(' ')[1][:2])
                await Questions.create(url=url, answer=answer, questions=question, ege_number=ege_number)




