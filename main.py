from map_crawler import Crawl
from map_scrapper import Scrape
import logging
import os

#Full List of State
State = ["Perlis",	"Kedah", "Kelantan", "Terengganu", "Pulau Pinang", "Perak",	"Pahang", "Selangor", "Negeri Sembilan", "Melaka", "Johor", "Sabah", "Sarawak",	"W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan"]
#Store to Scrape

def crawl(store, pagesource_dir, dataset_dir, state_list ):
    crawler = Crawl(store, pagesource_dir, dataset_dir, state_list)
    query_list, csv_file = crawler.get_query()
    while True:
        try:
            crawler.start_scrape(query_list, csv_file)
            break
        except Exception as e:
            logging.info(f"An exception occured while scraping: {e}.")
            error_message = str(e)
            failed_query = error_message.split("query :")[-1].strip()
            query_list = crawler.get_updated_query_list(failed_query, query_list)
            logging.info('Restarting Process')
            e.__cause__
def scrape(store, pagesource_dir, dataset_dir, state_list ):
    scraper = Scrape(store, pagesource_dir, dataset_dir, state_list )
    scraper.extract_source()

def start(store, state_list = State):
    directory = f"{store} Scrapper"
    log_dir = f"{directory}/log"
    dataset_dir = f"{directory}/dataset"
    pagesource_dir = f"{directory}/html_page_source"
    if not os.path.exists(directory):
        os.mkdir(directory)
        os.makedirs(log_dir)
        os.makedirs(dataset_dir)
        os.makedirs(pagesource_dir)

    logging.basicConfig(filename=f"{log_dir}/{store}_map_scrapper.log", encoding="utf-8", filemode="a",
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    crawl(store, pagesource_dir, dataset_dir, state_list )
    scrape(store, pagesource_dir, dataset_dir, state_list)
    
start("McDonald's")