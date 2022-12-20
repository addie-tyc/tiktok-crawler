import os

from dotenv import load_dotenv
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
options.binary_location = os.getenv('BINARY_LOC') # need to install chromium first

if __name__ == '__main__':
    driver = webdriver.Chrome(options=options)
    links = TiktokAccountCrawler('@archieandaxing', driver).run()
    TiktokPostsCrawler(links, driver).run()
    driver.close()
