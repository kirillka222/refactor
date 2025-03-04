from .. import edu_login
from bs4 import BeautifulSoup as BS
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def parse_homework_of_day(login: str, password: str, date: int) -> list[dict]:

    html_text = edu_login.get_url(login, password, f"https://edu.tatar.ru/user/diary/day?for={date}")
    html = BS(html_text, 'html.parser')
    count = len(html.select('#content > div.r_block > div > div > div.d-table > table > tbody > tr'))
    list_of_homework = list()
    for i in range(1, count + 1):
        time_of_lesson = html.select(
            f'#content > div.r_block > div > div > div.d-table > table > tbody > tr:nth-child({i}) > td:nth-child(1)'
        )[0].getText()
        object_ = html.select(
            f'#content > div.r_block > div > div > div.d-table > table > tbody > tr:nth-child({i}) > td:nth-child(2)'
        )[0].getText()
        homework = html.select(
            f'#content > div.r_block > div > div > div.d-table > table > tbody > tr:nth-child({i}) > td:nth-child(3)'
        )[0].getText()
        # Убираем лишние пробелы, переносы строки между словами
        object_ = " ".join(object_.replace('\n', ' ').split())
        homework = " ".join(homework.replace('\n', ' ').split())
        list_of_homework.append({
            "object": object_,
            "homework": homework,
            "time": time_of_lesson
        })
    return list_of_homework
