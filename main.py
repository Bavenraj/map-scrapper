from map_crawler import get_query, start_scrape, get_updated_query_list
from map_scrapper import extract_data, extract_source

#Full List of State
State = ["Perlis",	"Kedah", "Kelantan", "Terengganu", "Pulau Pinang", "Perak",	"Pahang", "Selangor", "Negeri Sembilan", "Melaka", "Johor", "Sabah", "Sarawak",	"W.P. Kuala Lumpur", "W.P. Putrajaya", "W.P. Labuan"]
#Store to Scrape
store = 'KFC'
query_list, csv_file = get_query(store, ["Perlis"])
while True:
    try:
        start_scrape(store, query_list, csv_file)
        break
    except Exception as e:
        #print(f"{e}")
        print(e)
        failed_query = e.args[0] 
        query_list = get_updated_query_list(failed_query, query_list)
