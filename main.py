import os

from dotenv import load_dotenv
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawlers.TiktokAccountCrawler import TiktokAccountCrawler
from crawlers.TiktokPostsCrawler import TiktokPostsCrawler

load_dotenv()

options = Options()
# for error: DevToolsActivePort file doesn't exist
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--headless')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    driver = webdriver.Chrome(options=options)
    for account in ['@archieandaxing', '@zachking']:
        posts = TiktokAccountCrawler(account, driver).run()
        TiktokPostsCrawler(account, driver, posts).run()
    driver.close()
    return 'ok', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
