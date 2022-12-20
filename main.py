from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from crawlers.TiktokAccountCrawler import TiktokAccountCrawler
from crawlers.TiktokPostsCrawler import TiktokPostsCrawler

options = Options() 
options.add_argument('--no-sandbox') # for error: DevToolsActivePort file doesn't exist
options.add_argument('--headless')  
options.add_argument('--disable-gpu')

if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    links = TiktokAccountCrawler('@archieandaxing', driver).run()
    TiktokPostsCrawler(links, driver).run()
    driver.close()
