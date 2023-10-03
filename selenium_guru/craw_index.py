import os
import sys
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
# from LyricSpider.src.utils import read_json, save_json
import random

# Set up the driver
options = webdriver.SafariOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  # Disabling the flag that identifies automation control
options.add_argument("--start-maximized")  # Start browser maximized

jpath = os.path.join

def _main():
    url = 'https://www.propertyguru.com.sg/property-for-rent?market=residential&beds[]=-1&listing_type=rent&minprice=800&maxprice=1200&MRT_STATIONS[]=EW24&MRT_STATIONS[]=JE5&MRT_STATIONS[]=NS1&MRT_STATIONS[]=EW23&MRT_STATIONS[]=EW22&MRT_STATIONS[]=CC22&MRT_STATIONS[]=EW21&MRT_STATIONS[]=EW20&MRT_STATIONS[]=EW19&MRT_STATIONS[]=EW18&MRT_STATIONS[]=EW17&MRT_STATIONS[]=EW16&MRT_STATIONS[]=NE3&MRT_STATIONS[]=TE17&MRT_STATIONS[]=EW15&MRT_STATIONS[]=CC21&MRT_STATIONS[]=CC20&MRT_STATIONS[]=CC19&MRT_STATIONS[]=DT9&MRT_STATIONS[]=CC23&MRT_STATIONS[]=CC24&MRT_STATIONS[]=CC25&freetext=EW24/NS1/JE5+Jurong+East+MRT,+EW23+Clementi+MRT,+EW22+Dover+MRT,+CC22/EW21+Buona+Vista+MRT,+EW20+Commonwealth+MRT,+EW19+Queenstown+MRT,+EW18+Redhill+MRT,+EW17+Tiong+Bahru+MRT,+EW16/NE3/TE17+Outram+Park+MRT,+EW15+Tanjong+Pagar+MRT,+CC21+Holland+Village+MRT,+CC20+Farrer+Road+MRT,+CC19/DT9+Botanic+Gardens+MRT,+CC23+One-North+MRT,+CC24+Kent+Ridge+MRT,+CC25+Haw+Par+Villa+MRT&search=true'
    out_dir = './download'
    crawl_index(url, out_dir)

def crawl_index(url, out_dir):
    '''
    Craw index according to url, save to indiate path
    '''
    page_cnt = 0

    # Prepare path
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    base_link = url
    link = base_link
    while link != None:
        page_cnt += 1
        print('Trying to crawl index page {} ...'.format(page_cnt))
        driver = webdriver.Safari()
        driver.get(link)
        
        sleep_s = random.uniform(1,2)
        time.sleep(sleep_s)
        driver.execute_script("window.scrollTo(0, 1000)")
        with open(jpath(out_dir, '{}.html'.format(page_cnt)), 'w') as f:
            f.write(driver.page_source)

        try:
            next_page_button =  driver.find_element(By.CSS_SELECTOR, '#search-results-container > div.container.search-result-inner-container > div.contents > div.columned-content > div.columned-content-row.main-content-wrapper > section > div.listing-pagination > ul > li.pagination-next > a')
            link = next_page_button.get_property('href')
        except:
            link = None
        driver.quit()
    print('Index crawling finished.')

if __name__ == '__main__':
    _main()
