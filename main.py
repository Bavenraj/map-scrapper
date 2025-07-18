from map_crawler import Crawl
from map_scrapper import Scrape
import logging

#Full List of State
State = ["Perlis",	"Kedah", "Kelantan", "Terengganu", "Pulau Pinang", "Perak",	"Pahang", "Selangor", "Negeri Sembilan", "Melaka", "Johor", "Sabah", "Sarawak",	"W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan"]
#Store to Scrape

def crawl(store):
    crawler = Crawl()
    logging.basicConfig(filename=f"log/{store}_map_crawler.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    query_list, csv_file = crawler.get_query(store)
    while True:
        try:
            crawler.start_scrape(store, query_list, csv_file)
            break
        except Exception as e:
            logging.info(f"An exception occured while scraping: {e.args[0]}")
            #print(f"{e}")
            print(e)
            failed_query = e.args[0] 
            query_list = crawler.get_updated_query_list(failed_query, query_list)
            logging.info('Restarting Process')
    
#crawl('KFC')

def scrape(store):
    scraper = Scrape(store)
    logging.basicConfig(filename=f"log/{store}_map_scrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    scraper.extract_source()

scrape('KFC')