import bs4
import requests
from collections import defaultdict
import time

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


def get_proxies_list():
    e = defaultdict(list)
    response = requests.get('http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo')
    lst = response.text.split()
    return lst


def fetch_afisha_page():
    response = requests.get('https://www.afisha.ru/msk/schedule_cinema/', headers={'user-agent': USER_AGENT})
    return response.text


def parse_afisha_list(raw_html):
    items = []
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    d = soup.select('.b-theme-schedule.b-theme-schedule .object')
    for item in d:
        film_name = item.select('.m-disp-table h3 a[href]')[0].string
        lst = item.select('.m-disp-table + table tr .b-td-item a')
        cinemas = [item.string for item in lst]
        items.append({
            'film_name': film_name,
            'cinemas': cinemas,
            'cinemas_count': len(cinemas)
        })
    return items


def fetch_movie_info(movie_title):
    s = requests.Session()
    #params = {'kp_query': movie_title, 'first': 'yes', 'what': ''}
    params = {'q': movie_title, 'topsuggest': 'true', 'ajax': 1}
    response = requests.get(
        'https://www.kinopoisk.ru/search/suggest',
        headers={'user-agent': USER_AGENT},
        params=params
    )
    #raw_html = response.json()
    raw_html = response.text
    print(raw_html)
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    datas = soup.find_all('span', attrs={'class': ['rating_ball', 'ratingCount']})
    print(datas)


def get_movie_id(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    raw_html = fetch_afisha_page()
    films = parse_afisha_list(raw_html)
    for film in films:
        time.sleep(2)
        film_id = fetch_movie_info(film['film_name'])
        film['film_id'] = film_id
