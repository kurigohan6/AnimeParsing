import urllib.request
from bs4 import BeautifulSoup
from time import sleep


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse_about(html):
    global anime_rating
    soup_about = BeautifulSoup(html, 'html.parser')
    table_about = soup_about.find('div', class_='scores')  # ищет раздел с балами
    current_about = table_about.find('meta', itemprop='ratingValue')  # находит сам балл
    anime_rating = current_about.get('content')  # получает значение
    sleep(1)  # засыпает чтобы сарвак не закрыл кран


def parse(html):
    soup_about = BeautifulSoup(html, 'html.parser')
    table = soup_about.find('tbody', class_='entries')
    anime = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')

        parse_about(get_html(cols[1].a.get('href')))  # получает ссылку на аниме и парсит страницу тайтла.

        anime.append({
            'title': cols[1].a.text,
            'total_rate': anime_rating,
            'user_rate': cols[2].span.text,
            'episodes': cols[3].span.text,
            'link': cols[1].a.get('href')
        })
    for project in anime:
        print(project)


def main():
    parse(get_html('http://shikimori.org/UltraKek/list/anime/mylist/completed/order-by/my'))  # вместо UltraKek свой ник


if __name__ == '__main__':
    main()
