from _Generic_Scrapers.QiqiScraper import QiqiScraper

site_url = 'http://www.cnba.live/'
site_name = '琦琦看新聞'
site_id = 'N6'

scraper = QiqiScraper(site_url, site_name, site_id)
scraper.run()




