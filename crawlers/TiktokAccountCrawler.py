from datetime import datetime
import os

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import pymysql.cursors

from crawlers.BaseTiktokCrawler import BaseTiktokCrawler
from logger import logger
from util import convert_str_to_number

load_dotenv()

class TiktokAccountCrawler(BaseTiktokCrawler):

    def __init__(self, account, driver):
        super().__init__(account, driver)
        self.url = f'https://www.tiktok.com/{self.account}'
        self.posts = []
    
    def crawl(self, url=None) -> dict:
        self.driver.get(self.url)
        html = bs(self.driver.page_source, 'html.parser')
        targets = [
                ('h2', {'data-e2e': 'user-title'}),
                ('h1', {'data-e2e': 'user-subtitle'}),
                ('h2', {'data-e2e': 'user-bio'}),
            ]
        counts = [
            ('strong', {'data-e2e': 'following-count'}),
            ('strong', {'data-e2e': 'followers-count'}),
            ('strong', {'data-e2e': 'likes-count'})
        ]
        res = self.parse_targets(html, targets, {})
        self.parse_targets(html, counts, res, convert_str_to_number)
        self.posts = self.get_latest_posts(html)
        logger.info(f'Get {len(self.posts)} latest posts.')
        utcnow = datetime.utcnow()
        res['created'] = utcnow
        filename = f'data/{self.account}/{utcnow}.html'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w+') as file:
            file.write(str(html))
        return res
    
    def save_to_db(self, data: dict):
        conn = pymysql.connect(
            host=os.getenv('SQL_HOST'),
            port=int(os.getenv('SQL_PORT')),
            user=os.getenv('SQL_USER'), 
            password=os.getenv('SQL_PWD'),
            db=os.getenv('SQL_DB')
            )
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        with conn.cursor() as cursor:
            sql = 'INSERT INTO `accounts_info` (%s) VALUES (%s)' % (columns, placeholders)
            cursor.execute(sql, list(data.values()))
        logger.info(f'`{data["user_title"]}` saved.')
        conn.commit()
        conn.close()

    def get_latest_posts(self, html, limit=5):
        posts = html.findAll('div', {'data-e2e': 'user-post-item'}, limit=limit)
        return [{
            'link': post.find('a')['href'], 
            **self.parse_targets(post, [('strong', {'data-e2e': 'video-views'})], {}, convert_str_to_number)
            } for post in posts]

    def run(self):
        res = self.crawl()
        self.save_to_db(res)
        return self.posts
