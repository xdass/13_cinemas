import bs4
import requests
from collections import defaultdict


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


def get_proxies_list():
    e = defaultdict(list)
    response = requests.get('http://www.freeproxy-list.ru/api/proxy?anonymity=false&token=demo')
    #lst = response.text.split()
    lst = ['87.103.234.116:3128', '176.53.248.63:3128', '92.38.47.226:80', '195.98.68.176:53281', '37.29.75.223:8080', '46.52.220.238:8080', '46.101.79.79:8118', '95.79.112.7:8080', '5.11.67.148:53281', '31.173.218.199:8080', '46.146.220.74:8080', '217.65.217.68:8080', '80.71.163.101:3128', '80.234.41.140:8080', '185.34.20.82:8080', '188.0.168.205:8080', '176.62.77.212:8080', '95.189.123.74:8080', '95.189.123.73:8080', '94.137.31.217:8080', '46.229.139.247:8080', '46.150.169.90:53281', '217.119.82.14:8080', '83.171.109.200:8080', '46.101.90.139:8118', '78.25.98.114:8080', '95.165.164.170:53281', '195.209.125.98:53281', '93.180.7.246:8080', '188.128.1.37:8080']
    return lst


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
    # with open('content_for_test.html', encoding='utf-8') as file:
    #     soup = bs4.BeautifulSoup(file, 'html.parser')
    # d = soup.select('.b-theme-schedule.b-theme-schedule .object')
    # for item in d:
    #     film_name = item.select('.m-disp-table h3 a[href]')[0].string
    #     lst = item.select('.m-disp-table + table tr .b-td-item a')
    #     cinemas = [item.string for item in lst]
    #     items.append({
    #         'film_name': film_name,
    #         'cinemas': cinemas,
    #         'cinemas_count': len(cinemas)
    #     })
    # r = requests.get('https://www.kinopoisk.ru/index.php', params={'kp_query': 'Осколки', 'first': 'yes', 'what': ''})
    # print(r.text)
    # with open('kinopoisk.html', encoding='utf-8') as file:
    #     soup = bs4.BeautifulSoup(file, 'html.parser')
    # datas = soup.find_all('span', attrs={'class': ['rating_ball', 'ratingCount']})
    proxy_list = get_proxies_list()
    print(requests.get('https://api.ipify.org', headers={'user-agent': USER_AGENT}, proxies={'http': proxy_list, 'https': '176.53.248.63:3128'}).text)