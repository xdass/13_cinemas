from operator import itemgetter
import argparse
import bs4
import requests


def fetch_afisha_page():
    url = 'https://www.afisha.ru/msk/schedule_cinema/'
    response = make_data_request(url)
    return response.text


def make_data_request(url, params=None):
    user_agent = '''Mozilla/5.0 (Windows NT 6.1; Win64; x64)
                 AppleWebKit/537.36 (KHTML, like Gecko)
                 Chrome/62.0.3202.94 Safari/537.36'''
    response = requests.get(url, params=params, headers={'User-Agent': user_agent})
    return response


def parse_afisha_html(raw_html, movies_to_parse):
    movies_info = []
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    movies_html = soup.select('.b-theme-schedule.b-theme-schedule .object')
    for movie_html in movies_html[:movies_to_parse]:
        film_name = movie_html.select_one('.m-disp-table h3 a[href]').string
        cinemas_ahref_list = movie_html.select('.m-disp-table + table tr .b-td-item a')
        movies_info.append({
            'film_name': film_name,
            'cinemas_count': len(cinemas_ahref_list)
        })
    return movies_info


def fetch_movie_id(movie_title):
    url = 'https://www.kinopoisk.ru/search/suggest'
    params = {'q': movie_title, 'topsuggest': 'true', 'ajax': 1}
    response = make_data_request(url, params)
    movie_json_info = response.json()
    if movie_json_info:
        if movie_json_info[0]['dataType'] == 'film':
            return movie_json_info[0]['id']


def fetch_movie_rating(movie_id):
    url = 'https://rating.kinopoisk.ru/{}.xml'.format(movie_id)
    response = make_data_request(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    rating = soup.kp_rating.text
    num_voice = soup.kp_rating['num_vote']
    return num_voice, rating


def collect_full_movies_info(movies):
    full_movies_info = []
    for movie in movies:
        film_id = fetch_movie_id(movie['film_name'])
        if film_id:
            num_voice, rating = fetch_movie_rating(film_id)
            movie['num_voice'] = num_voice
            movie['rating'] = rating
            full_movies_info.append(movie)
    return full_movies_info


def output_movies_to_console(movies, min_in_cinemas):
    movies.sort(key=itemgetter('rating'), reverse=True)
    if min_in_cinemas:
        movies = [movie_info for movie_info in movies if movie_info['cinemas_count'] > min_in_cinemas]
    for movie in movies:
        print(movie['film_name'])
        print('Рейтинг фильма(кинопоиск): {}'.format(movie['rating']))
        print('Проголосовало: {}'.format(movie['num_voice']))
        print('Идет в {} кинотеатрах'.format(movie['cinemas_count']))
        print('-------------------------------------------------------')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program to get movies info')
    parser.add_argument(
        '--movies_count',
        default=10,
        type=int,
        help='Amount of movies that will be parse(default is 10)'
    )
    parser.add_argument(
        '--min_in',
        default=None,
        type=int,
        help='Minimum amount of cinemas where movie show(default is None)'
    )
    args = parser.parse_args()
    print('Load afisha...')
    raw_html = fetch_afisha_page()
    print('Parsing movies from afisha...')
    movies_from_afisha = parse_afisha_html(raw_html, args.movies_count)
    print('Getting full movies info...')
    movies_full_data = collect_full_movies_info(movies_from_afisha)
    output_movies_to_console(movies_full_data, args.min_in)
