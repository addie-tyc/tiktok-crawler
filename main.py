from crawlers.TiktokAccountCrawler import TiktokAccountCrawler
from crawlers.TiktokPostsCrawler import TiktokPostsCrawler

if __name__ == '__main__':
    links = TiktokAccountCrawler('@archieandaxing').run()
    TiktokPostsCrawler(links).run()
