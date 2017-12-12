import bs4
import requests


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'

# .m-disp-table h3 a Film tag


def fetch_afisha_page():
    pass


def parse_afisha_list(raw_html):
    pass


def fetch_movie_info(movie_title):
    pass


def output_movies_to_console(movies):
    pass


if __name__ == '__main__':
    items = []
    with open('content_for_test.html', encoding='utf-8') as file:
        soup = bs4.BeautifulSoup(file, 'html.parser')
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