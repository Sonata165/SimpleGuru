from utils import *
import pandas as pd


def main():
    info_fp = './info_aug.json'
    out_fp = 'data.csv'

    rank(info_fp, out_fp)

def rank(info_fp, out_fp, hparam=None):
    data = read_json(info_fp)

    # Data type convert
    for id in data:
        entry = data[id]
        data[id]['price'] = int(entry['price'])
        data[id]['size'] = min(max(int(entry['size']), hparam['size']['worst']), hparam['size']['best'])
        try:
            year = int(entry['top_year'].strip().split(' ')[-1])
            data[id]['top_year'] = min(max(year, hparam['year']['worst']), hparam['year']['best'])
        except:
            data[id]['top_year'] = 2000
        try:
            data[id]['psf'] = float(entry['psf'])
        except:
            data[id]['psf'] = 5
        
        data[id]['time_to_work'] = norm_time_to_min(entry['time_to_work'])
        data[id]['time_to_xx'] = norm_time_to_min(entry['time_to_xx'])

    # Normalize by range: 
    df = pd.DataFrame.from_dict(data, orient='index')
    for k in ['size', 'top_year']:
        k_n = k + '_n'
        df[k_n] = normalize_column(df[k])
    data_n = df.to_dict(orient='index')

    # Compute score for each entry
    for id in data:
        entry = data[id]
        entry_n = data_n[id]
        score = compute_score(entry_n, hparam)
        data[id]['score'] = score

    # Sort by score
    data = dict(sorted(data.items(), key=lambda item: item[1]['score'], reverse=True))

    # Put score to front
    data = {k: {'score': v['score'], **{kk: vv for kk, vv in v.items() if kk != 'score'}} for k, v in data.items()}
    
    # Convert to CSV
    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_csv(out_fp, index=False)  

def norm_time_to_min(time_str):
    work_time = time_str.split(' ')
    if len(work_time) <= 2:
        work_h = 0
        work_m = int(work_time[0])
    else:
        work_h = int(work_time[0])
        work_m = int(work_time[2])
    work_min = work_h * 60 + work_m
    return work_min

def compute_score(entry, hparam):
    '''
    Compute score, considering price, size, top_year, sexist, is_master, time_to_work, time_to_XX
    psf not included
    '''
    if hparam['i_am_girl']:
        s_sexist = 1
    else:
        s_sexist = 0 if entry['sexist'] == True else 1
    if not hparam['require_aircon']:
        s_aircon = 1
    else:
        s_aircon = 0 if entry['no_aircon'] else 1

    s_price = number_to_score(entry['price'], hparam['price']['best'], hparam['price']['worst'], False)
    s_size = 1 - entry['size_n']
    s_year = entry['top_year_n']
    s_master = 1 if entry['is_master'] else 0
    s_time_work = number_to_score(entry['time_to_work'], hparam['work_1_time']['best'], hparam['work_1_time']['worst'], False)
    s_time_xx = number_to_score(entry['time_to_xx'], hparam['work_2_time']['best'], hparam['work_2_time']['worst'], False)
    

    weights = hparam['weights']
    tot = sum([weights[i] for i in weights])
    score = (s_price*weights['price'] + s_size*weights['size'] + s_year*weights['year'] 
            + s_master*weights['master'] + s_time_work*weights['time_work'] + s_time_xx*weights['time_xx']) / tot
    return score * s_sexist * s_aircon

def normalize_column(column):
    min_value = column.min()
    max_value = min(column.max(), 2020)
    normalized_column = (column - min_value) / (max_value - min_value)
    return normalized_column

def number_to_score(n, best, worst, higher_better):
    if higher_better == True:
        assert best > worst
        score = max((n - worst), 0) / (best - worst)
    else:
        assert worst > best
        score = 1 - min(max((n - best), 0) / (worst - best), 1)
    return score

if __name__ == '__main__':
    main()