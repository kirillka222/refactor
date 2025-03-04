from .. import edu_login
from bs4 import BeautifulSoup as BS
from fastapi import APIRouter

router = APIRouter()


def clean_html(html_text: str) -> BS:
    return BS(html_text.replace('&mdash;', ''), 'html.parser')


def extract_text(html: BS, selector: str) -> str:
    element = html.select_one(selector)
    return element.get_text(strip=True) if element else ""


def parse_school_info(school_page: str) -> str:
    html = clean_html(school_page)
    selector = (
        'body > div.container > div.row > #cabinet > div.col-md-9.col > div > '
        'div.panel-body > div > div.col-md-9 > div > #frm > table > tr:nth-child(5) > td:nth-child(2)'
    )
    return extract_text(html, selector)


def parse_class_info(marks_page: str) -> str:
    html = clean_html(marks_page)
    selector = '#content > div.r_block > div > div > p:nth-child(2)'
    class_text = extract_text(html, selector)
    return class_text.split('Класс: ')[1] if 'Класс: ' in class_text else ""


def parse_medium_score(marks_page: str) -> float:
    html = clean_html(marks_page)
    marks_rows = html.select('#content > div.r_block > div > div > div > table > tbody > tr')
    selector = f'#content > div.r_block > div > div > div > table > tbody > tr:nth-child({len(marks_rows)}) > td'
    medium_text = extract_text(html, selector)
    try:
        return float(medium_text)
    except ValueError:
        return 0.0


@router.get("/")
def get_information_about_school_and_class(login: str, password: str) -> tuple[str, str, float]:
    urls = [
        'https://edu.tatar.ru/user/anketa/edit',
        'https://edu.tatar.ru/user/diary/term'
    ]
    school_page, marks_page = edu_login.get_urls(login, password, urls)

    school = parse_school_info(school_page)
    class_ = parse_class_info(marks_page)
    medium = parse_medium_score(marks_page)

    return school, class_, medium
