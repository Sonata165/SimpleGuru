import os
import time
import platform
import mlconfig

from selenium_guru.craw_index import crawl_index
from selenium_guru.index_parser import parse_index
from selenium_guru.craw_info import craw_property_info
from selenium_guru.info_parser import parse_info
from selenium_guru.augment_property import augment_info
from selenium_guru.rank import rank

jpath = os.path.join

def main(hparam):

    # Crawl index
    if hparam['do_crawl_index']:
        print('Start crawling ...')
        crawl_index(hparam['index_url'], out_dir=hparam['out_index_dir'])
    else:
        print('Index crawling skipped.')

    # Parse index
    if hparam['do_parse_index']:
        print('Parse index ...')
        parse_index(data_dir=hparam['out_index_dir'], out_path=hparam['out_index_fp'])
    else:
        print('Index parsing skipped.')

    # Crawl property info
    if hparam['do_crawl_properties']:
        print('Crawl property info ...')
        craw_property_info(index_fp=hparam['out_index_fp'], out_dir=hparam['out_info_dir'])
    else:
        print('Info crawling skipped')

    # Parse property info
    if hparam['do_parse_properties']:
        print('Parse property info ...')
        parse_info(hparam['out_info_dir'], hparam['out_info_fp'], hparam['out_index_fp'])
    else:
        print('Info parsing skipped')

    # Augment property info
    if hparam['do_augment_info']:
        print('Augment property info ...')
        augment_info(hparam['out_info_fp'], hparam['aug_out_fp'], hparam)
    else:
        print('Info augmentation skipped')

    # Rank properties
    if hparam['do_rank']:
        print('Start ranking ...')
        rank(info_fp=hparam['aug_out_fp'], out_fp=hparam['rank_out_fp'], hparam=hparam)
    else:
        print('Ranking skipped.')
    
    print('Finish. Good luck. ')


if __name__ == '__main__':
    machine = platform.platform().split('-')[0]  # macOS | Linux
    if machine == 'macOS':  # Local
        arg_path = './private/my_conf.yaml'
        hparam = mlconfig.load(arg_path)
    else:
        raise NotImplementedError()


    # Prepare dir
    print('Debug mode:', hparam['debug'])
    if hparam['debug']:
        hparam['output_dir'] = hparam['output_dir']+'_debug'
    hparam['log_fn'] = jpath(hparam['output_dir'], 'log.txt')
    if not os.path.exists(hparam['output_dir']):
        os.makedirs(hparam['output_dir'])

    main(hparam)


