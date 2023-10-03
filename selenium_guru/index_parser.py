# from html.parser import HTMLParser
import scrapy
from scrapy.selector import Selector
from utils import print_json, read_json, save_json, ls, jpath

def main():
    data_dir = './download/index/'
    out_path = './download/index.json'

    parse_index(data_dir, out_path)

def parse_index(data_dir, out_path):
    fns = ls(data_dir)
    fns.sort()

    ret = []
    ret = {}

    for fn in fns:
        fpath = jpath(data_dir, fn)
        data_path = fpath
        with open(data_path) as f:
            html = f.read()
        s = 'div.col-xs-12.col-sm-7.listing-description'
        s = s + ' h3 > a'
        s_href = s + '::attr(href)'
        s_title = s + '::attr(title)'
        res_href = Selector(text=html).css(s_href).getall()
        res_title = Selector(text=html).css(s_title).getall()
        res = list(zip(res_title, res_href))

        for title, url in res:
            id = url.strip().split('-')[-1]
            ret[id] = [title, url]

    print('Total No. Properties:', len(ret))
    save_json(ret, out_path)

if __name__ == '__main__':
    main()
