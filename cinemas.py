from operator import itemgetter
import argparse
import bs4
import requests


def fetch_afisha_page():
    url = 'https://www.afisha.ru/msk/schedule_cinema/'
    response = url_request(url)
    return response.text


def url_request(url, params=None):
    user_agent = ("Mozilla/5.0 (Windows NT 6.1;Win64; x64)"
                  "AppleWebKit/537.36(KHTML, like Gecko)"
                  "Chrome/62.0.3202.94 Safari/537.36")
    response = requests.get(url, params=params, headers={
        'User-Agent': user_agent,
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    })
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


def fetch_movie_page(movie_title):
    url = 'https://www.kinopoisk.ru/index.php'
    params = {'kp_query': movie_title, 'first': 'yes', 'what': ''}
    response = url_request(url, params)
    return response.text


def parse_film_id(film_html):
    soup = bs4.BeautifulSoup(film_html, 'html.parser')
    film_id = soup.select_one('button[data-film-id]').attrs['data-film-id']
    return film_id


def fetch_movie_rating(movie_id):
    url = 'https://rating.kinopoisk.ru/{}.xml'.format(movie_id)
    response = url_request(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    rating = soup.kp_rating.text
    num_voice = soup.kp_rating['num_vote']
    return num_voice, rating


def collect_full_movies_info(movies):
    full_movies_info = []
    for movie in movies:
        film_html = fetch_movie_page(movie['film_name'])
        film_id = parse_film_id(film_html)
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
        default=5,
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
