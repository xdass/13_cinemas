import time
from operator import itemgetter
import argparse
import bs4
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


def fetch_afisha_page():
    response = requests.get('https://www.afisha.ru/msk/schedule_cinema/', headers={'user-agent': USER_AGENT})
    return response.text


def parse_afisha_list(raw_html):
    movies_info = []
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    movies_html = soup.select('.b-theme-schedule.b-theme-schedule .object')
    for item in movies_html:
        film_name = item.select('.m-disp-table h3 a[href]')[0].string
        cinemas_ahref_list = item.select('.m-disp-table + table tr .b-td-item a')
        cinemas = [cinema_ahref.string for cinema_ahref in cinemas_ahref_list]
        movies_info.append({
            'film_name': film_name,
            'cinemas': cinemas,
            'cinemas_count': len(cinemas)
        })
    return movies_info


def get_movie_id(movie_title):
    params = {'q': movie_title, 'topsuggest': 'true', 'ajax': 1}
    response = requests.get(
        'https://www.kinopoisk.ru/search/suggest',
        headers={'user-agent': USER_AGENT},
        params=params
    )
    movie_json_info = response.json()
    if movie_json_info[0]['dataType'] == 'film':
        return movie_json_info[0]['id']
    else:
        return None


def get_movie_rating(movie_id):
    response = requests.get('https://rating.kinopoisk.ru/{}.xml'.format(movie_id))
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    rating = soup.kp_rating.text
    num_voice = soup.kp_rating['num_vote']
    return num_voice, rating


def collect_full_movie_info(movies):
    full_movies_info = []
    for film in movies:
        time.sleep(1)
        film_id = get_movie_id(film['film_name'])
        if film_id:
            num_voice, rating = get_movie_rating(film_id)
            film['num_voice'] = num_voice
            film['rating'] = rating
            full_movies_info.append(film)
    return full_movies_info


def output_movies_to_console(movies, movies_to_print, min_in_cinemas):
    movies.sort(key=itemgetter('rating'), reverse=True)
    if min_in_cinemas:
        movies = [movie_info for movie_info in movies if movie_info['cinemas_count'] > min_in_cinemas]
    for movie in movies[:movies_to_print]:
        print(movie['film_name'])
        print('Рейтинг фильма(кинопоиск): {}'.format(movie['rating']))
        print('Проголосовало: {}'.format(movie['num_voice']))
        print('Идет в {} кинотеатрах'.format(movie['cinemas_count']))
        print('-'*30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program to get movies info')
    parser.add_argument(
        '--movies_count',
        default=10,
        type=int,
        help='Amount of movies that will be print(default is 10)'
    )
    parser.add_argument(
        '--min_in',
        default=None,
        type=int,
        help='Minimum amount of cinemas where movie show(default is None)'
    )
    args = parser.parse_args()
    print(args)
    print('Load afisha...')
    raw_html = fetch_afisha_page()
    print('Parsing movies from afisha...')
    movies_from_afisha = parse_afisha_list(raw_html)
    print('Getting full movies info...')
    movies_full_data = collect_full_movie_info(movies_from_afisha)
    output_movies_to_console(movies_full_data, args.movies_count, args.min_in)
