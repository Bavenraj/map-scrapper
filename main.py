from map_crawler import Crawl
from map_scrapper import Scrape
import logging

#Full List of State
State = ["Perlis",	"Kedah", "Kelantan", "Terengganu", "Pulau Pinang", "Perak",	"Pahang", "Selangor", "Negeri Sembilan", "Melaka", "Johor", "Sabah", "Sarawak",	"W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan"]
#Store to Scrape

def crawl(store, state_list):
    crawler = Crawl(store, state_list)
    query_list, csv_file = crawler.get_query()
    while True:
        try:
            crawler.start_scrape(query_list, csv_file)
            break
        except Exception as e:
            logging.info(f"An exception occured while scraping: {e.args[0]}")
            #print(f"{e}")
            print(e)
            failed_query = e.args[0] 
            query_list = crawler.get_updated_query_list(failed_query, query_list)
            logging.info('Restarting Process')
    
def scrape(store, state_list ):
    scraper = Scrape(store, state_list)
    scraper.extract_source()

def start(store, state_list):
    logging.basicConfig(filename=f"log/{store}_map_scrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    crawl(store, state_list)
    scrape(store, state_list)
    
start('KFC', ["W.P. Labuan"])