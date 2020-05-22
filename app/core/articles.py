from datetime import datetime
from bs4 import BeautifulSoup
import requests

def get_all_articles(post_sitemap):
    r = requests.get(post_sitemap)
    post_sitemap_xml = r.text

    post_sitemap_soup = BeautifulSoup(post_sitemap_xml, 'lxml')
    sitemap_url_sections = post_sitemap_soup.find_all("url")

    posts = dict()

    for section in sitemap_url_sections:
        url = section.findNext("loc").text
        lastmod = section.findNext("lastmod").text

        r = requests.get(url)
        post_html = r.text
        soup = BeautifulSoup(post_html, 'lxml')

        title = soup.find_all('h1', {"class": "entry-title"})[0].text

        posts[title] = (url, lastmod)

    return posts


def update_articles(post_sitemap, app):
    articles = get_all_articles(post_sitemap)
    app.logger.info('Posts updated at: %s' % datetime.now())
    setattr(app, 'articles', articles)
