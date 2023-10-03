import os
import sys
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
# from LyricSpider.src.utils import read_json, save_json
import random
from tqdm import tqdm

from utils import *

# Set up the driver
options = webdriver.SafariOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  # Disabling the flag that identifies automation control
options.add_argument("--start-maximized")  # Start browser maximized

def _main():
    index_fp = './download/index.json'
    out_dir = './download/info'

    craw_property_info(index_fp, out_dir)

def craw_property_info(index_fp, out_dir):
    data = read_json(index_fp)
    data_l = list(data.items())
    data_l.sort()
    data = dict(data_l)

    # Prepare dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pbar = tqdm(data)
    for id in pbar:
        entry = data[id]
        title, url = entry
        id = url.strip().split('-')[-1]
        pbar.set_description('ID: {}'.format(id))
        out_fp = jpath(out_dir, '{}.html'.format(id))

        if not os.path.exists(out_fp):
            driver = webdriver.Safari()
            driver.get(url)
            time.sleep(1)
            with open(out_fp, 'w') as f:
                f.write(driver.page_source)
            driver.quit()
        else:
            pass
        
    print('Info crawling finished.')


if __name__ == '__main__':
    _main()
