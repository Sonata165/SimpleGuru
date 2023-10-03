# from html.parser import HTMLParser
import scrapy
from scrapy.selector import Selector
from utils import print_json, read_json, save_json, ls, jpath
from tqdm import tqdm

def main():
    data_dir = './download/info'
    out_path = './info.json'
    index_path = None

    parse_info(data_dir, out_path, index_path)

def parse_info(data_dir, out_path, index_path):
    index_data = read_json(index_path)

    fns = ls(data_dir)
    fns.sort()

    res = {}

    for fn in tqdm(fns):
        # Skip inactive properties
        id = fn.strip().split('.')[0]
        if id not in index_data:
            print(fn, 'not active')
            continue

        fpath = jpath(data_dir, fn)
        data_path = fpath
        with open(data_path) as f:
            html = f.read()
        
        # url
        s = 'meta[property="og:url"]::attr(content)'
        url = Selector(text=html).css(s).getall()[0]

        # title
        s = 'div.col-lg-8.col-md-12 div.property-overview-section.row h1::text'
        title = Selector(text=html).css(s).getall()[0]
        
        # location
        s = 'div.col-lg-8.col-md-12 > div > div > div.property-overview-section.row > div > div.location-info > div.full-address > p::text'
        location = Selector(text=html).css(s).getall()[0]

        # price
        s = 'div.col-lg-8.col-md-12 > div > div > div.property-overview-section.row > div > div.property-info > div.price-summary > div > h2::text'
        price = Selector(text=html).css(s).getall()[-1].strip().split(' ')[1].replace(',','')

        # abstract
        s = 'div:nth-child(5) > div > div.col-lg-8.col-md-12 > div > div > section.about-section > div > h3::text'
        abstract = Selector(text=html).css(s).getall()[0]

        # description
        s = 'meta[property="og:description"]::attr(content)'
        description = abstract + '\n' + Selector(text=html).css(s).getall()[0]

        # size
        s = 'div.col-lg-8.col-md-12 > div > div > section.details-section > section > div.meta-table-root > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > div.meta-table__item__value.col-md-12.col-7 > div::text'
        size = Selector(text=html).css(s).getall()[0].strip().split(' ')[0]

        # furnish
        s = 'div.col-lg-8.col-md-12 > div > div > section.details-section > section > div.meta-table-root > table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div > div.meta-table__item__value.col-md-12.col-7 > div::text'
        furnish = Selector(text=html).css(s).getall()[0]

        # top
        s = 'div.col-lg-8.col-md-12 > div > div > section.details-section > section > div.meta-table-root > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div > div.meta-table__item__value.col-md-12.col-7 > div::text'
        top = Selector(text=html).css(s).getall()[0]

        # psf
        s = 'div.col-lg-8.col-md-12 > div > div > section.details-section > section > div.meta-table-root > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div > div.meta-table__item__value.col-md-12.col-7 > div::text'
        psf = Selector(text=html).css(s).getall()[0].strip().split(' ')[1]

        # availability
        try:
            s = 'div.col-lg-8.col-md-12 > div > div > section.details-section > section > div.meta-table-root > table > tbody > tr:nth-child(5) > td:nth-child(2) > div > div > div.meta-table__item__value.col-md-12.col-7 > div::text'
            available = Selector(text=html).css(s).getall()[0]
        except:
            available = None

        # id
        id = url.split('-')[-1]

        # is_active

        res[id] = {
            'title': title,
            'url': url,
            'location': location,
            'price': price,
            'size': size,
            'availability': available,
            'description': description,
            'top_year': top,
            'furnish': furnish,
            'psf': psf,
        }

    save_json(res, out_path) 

if __name__ == '__main__':
    main()
