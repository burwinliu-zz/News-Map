from webpage.webscraping import scraper
if __name__ == '__main__':
    scraped_page = scraper.Headlines()
    print(scraped_page)