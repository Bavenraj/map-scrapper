from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from area_to_scrape import area_to_scrape_dict
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from file_modifier import get_file, write_file

class Crawl:
    def __init__(self, store, state_list = area_to_scrape_dict):
        logging.info('--Web Crawling--')
        logging.info("Initializing WebDriver")
        options = Options()
        options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.fieldnames = ['Store', 'State', 'Area', 'Count', 'Duration']
        self.store = store
        self.state_to_scrape = state_list

    def load_map(self):
        logging.info("Loading Google Maps")
        self.driver.get("https://www.google.com/maps/@4.619127,108.9124153,6z?entry=ttu&g_ep=EgoyMDI1MDYxNy4wIKXMDSoASAFQAw%3D%3D")
        time.sleep(3)

    def find_state(self, state):
        logging.info("Getting input search box")
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchboxinput')))
            
        input = self.driver.find_element(by = By.CLASS_NAME, value = "searchboxinput")
        input.clear()
        
        logging.info(f"Searching for {state}:")
        input.send_keys(state, Keys.ENTER)
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3) 
        
        logging.info("Looking for nearby location button")
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Nearby']")))
        NearbyButton = self.driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Nearby']")
        NearbyButton.click()
        time.sleep(1)
        
    def find_nearby_location(self, query):    
        
        logging.info("Getting nearby location input search box ")
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        input = self.driver.find_element(by=By.ID, value = "searchboxinput")
        input.clear()
        
        logging.info(f"Searching for {query}:")
        input.send_keys(query, Keys.ENTER)
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)
        logging.info("Looking for Searched Results")
        while True:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='Results for {query}']")))
                return self.scrape_results(query)
                
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "lfPIob")))
                    return self.scrape_result(query)
                    
                except TimeoutException:
                    pass
        
    def scrape_results(self, query):
        all_stores_detail = []
        scrollableElement = self.driver.find_element(by=By.CSS_SELECTOR, value =f"[aria-label='Results for {query}']")
        final_count = 0
        logging.info("Found. Scrolling search results list")
        while True:
            for _ in range(3):
                self.driver.execute_script('arguments[0].scrollBy(0,1000);', scrollableElement)
                time.sleep(1)
                
            try:
                if self.driver.find_element(by=By.CLASS_NAME, value = "PbZDve"):
                    result_found = self.driver.find_elements(by=By.CLASS_NAME, value = "hfpxzc")
                    final_count = len(result_found)
                    logging.info(f"Total of {final_count} stores found at {query} ")
                    break 
            except NoSuchElementException:
                pass

        self.driver.execute_script("arguments[0].scrollTop=0;", scrollableElement)
        time.sleep(1.5)
        
        logging.info(f"Extracting source of {final_count} stores")
        for result in result_found:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", result)
            time.sleep(0.5)
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(result))
            result.click()
            #removed while true loop
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "lfPIob")))
            while True:          
                page_html = self.driver.page_source
                soup = BeautifulSoup(page_html, "html.parser")
                store_name = soup.find(name='h1', attrs={"class":"lfPIob"}).text
                store_details = soup.find(name= 'div', attrs={"class": "lMbq3e"})
                store_region = soup.find(name='div', attrs={"aria-label":f"Information for {store_name}"})
                if None not in [store_name, store_details, store_region]:
                    break
                else:
                    pass
            all_stores_detail.append(str(f"<div class='store_details'>{store_details} {store_region}</div>"))
            logging.info(f"Store: {store_name} completed.") 
            self.driver.find_element(by=By.CSS_SELECTOR, value = f"[data-disable-idom = 'true']").click()
            while True:
                try:
                    WebDriverWait(self.driver, 2).until(EC.invisibility_of_element((By.CLASS_NAME, "lfPIob")))
                    WebDriverWait(self.driver, 2).until(EC.invisibility_of_element((By.CSS_SELECTOR, "[data-item-id = 'address']")))
                    break
                except TimeoutException:
                    pass
                
        logging.info("Combining Page Sources")
        with open(f"scraped_pagesource/{query}.html", "w", encoding="utf-8") as file:
            file.write(f"<html><head><meta charset='utf-8'></head><body>{''.join(all_stores_detail)}</body><html>")
        logging.info(f"{query}: {final_count}")
        
        return final_count
        
    def scrape_result(self, query):
        logging.info("Result list not found. Only One Result available")
        time.sleep(2)
        logging.info("Extracting Page Source")
        #removed while true loop
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "lfPIob")))

        while True:          
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")
            store_name = soup.find(name='h1', attrs={"class":"lfPIob"}).text
            store_details = soup.find(name= 'div', attrs={"class": "lMbq3e"})
            store_region = soup.find(name='div', attrs={"aria-label":f"Information for {store_name}"})
            if None not in [store_name, store_details, store_region]:
                break
            else:
                pass
        with open(f"scraped_pagesource/{query}.html", "w", encoding="utf-8") as file:
            file.write(page_html)
        final_count = 1
        logging.info(f"{query}: {final_count}")
        return final_count
            
    def get_query(self):

        query_list = []
        file_name = f'dataset/list_of_{self.store}_by_area.csv'
        
        filtered_dict = {}
        for state, areas in area_to_scrape_dict.items():
            if state in self.state_to_scrape:
                filtered_dict[state] = areas
        csv_file = get_file(file_name, self.fieldnames, filtered_dict)      
        for state, areas in filtered_dict.items():
            for area in areas:
                query = f"{self.store} near {area}, {state}"
                query_list.append(query)
        return query_list, csv_file 

    def get_updated_query_list(self, query, query_list):
        logging.info(f"Updating query list starting with failed query: {query}")
        failed_at_index = query_list.index(query)
        return query_list[failed_at_index:]

    def start_scrape(self, query_list, csv_file):
        store_count = []
        for query in query_list:
            store_data = []
            try:
                area = query.split('near', 1)
                state = area[1].split(',', 1)
                start_time = time.perf_counter()
                self.load_map()
                self.find_state(state[1])
                store_count.append(self.find_nearby_location(query = query))
                end_time = time.perf_counter()
                scraping_duration = end_time - start_time
                data_link = {
                    'Store': self.store,
                    'State': state[1],
                    'Area' : area[1],
                    'Count': store_count[-1],
                    'Duration': round(scraping_duration, 2)
                }
                store_data.append(data_link) 
                    
                write_file(csv_file, self.fieldnames, store_data)    
                logging.info(f"{self.store} data for {query} was loaded into csv")
            except Exception as e:
                raise Exception(query)
    #print(store_data)
