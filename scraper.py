import string
import os
import requests as re
from bs4 import BeautifulSoup

URL = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
DOMAIN = "https://www.nature.com"
headers = {'Accept-Language': 'en-US,en;q=0.5'}


def get_scrap_details():
    page_no = int(input())
    article_type = input()
    return page_no, article_type


def scrap_article(article, directory):
    file_name = article[0] + ".txt"
    link = DOMAIN + article[1]
    header = {'Accept-Language': 'en-US,en;q=0.5'}
    article_page = re.get(link, headers=header)
    soup = BeautifulSoup(article_page.content, 'html.parser')
    summary = soup.find('p', {'class': 'article__teaser'}).string

    full_path = os.path.normpath(directory + "/" + file_name)
    file = open(full_path, 'wb')
    file.write(bytes(str(summary), encoding='utf-8'))
    file.close()
    print("SUCCESS:", article)


def create_dictionary(current_page):
    dir_name = "Page_" + str(current_page)
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
    finally:
        return dir_name


def main():
    page_no, article_type = get_scrap_details()
    articles_found = []

    for current_page in range(1, page_no + 1):
        articles_found = []
        full_url = URL + str(current_page)
        page = re.get(full_url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all('article')

        for a in articles:
            if a.find('span', {'data-test': 'article.type'}).span.string == article_type:
                articles_found.append(a)

        articles_to_scrap = {}
        curr_dictrionary = create_dictionary(current_page)
        for af in articles_found:
            title = str(af.a.string).translate(str.maketrans('', '',
                                                             string.punctuation)).strip().replace(' ', '_')
            link = af.a.get('href')
            articles_to_scrap[title] = link

        for article in articles_to_scrap.items():
            scrap_article(article, curr_dictrionary)

if __name__ == "__main__":
    main()
