import sys
from utils import *
import subprocess
from tqdm import tqdm

def main():
    info_fp = './info.json'
    aug_out_fp = './info_aug.json'

    augment_info(info_fp, aug_out_fp)

def augment_info(info_fp, aug_out_fp, hparam=None):
    data = read_json(info_fp)
    lady_cnt = 0
    dur_util = DurUtil(hparam)
    pbar = tqdm(data)
    for id in pbar:
        pbar.set_description('ID: {}'.format(id))
        entry = data[id]
        
        t = entry['description'].strip().lower().replace('\n', '')

        if 'female' in t or 'lady' in t or 'ladies' in t or 'fenale' in t:
            data[id]['sexist'] = True
            lady_cnt += 1
        else:
            data[id]['sexist'] = False

        if 'master room' in t:
            data[id]['is_master'] = True
        else:
            data[id]['is_master'] = False

        if 'no aircon' in t:
            data[id]['no_aircon'] = True
        else:
            data[id]['no_aircon'] = False

        address = entry['location']
        
        res = dur_util.compute_dur(address, hparam['place_work_1'])
        time1 = res['routes'][0]['localizedValues']['duration']['text'] # Transit time for work

        res = dur_util.compute_dur(address, hparam['place_work_2'])
        time2 = res['routes'][0]['localizedValues']['duration']['text'] # Transit time for XX
            
        data[id]['time_to_work'] = time1
        data[id]['time_to_xx'] = time2

        
    print('{}/{} for lady only'.format(lady_cnt, len(data)))
    dur_util.save_alias()
    save_json(data, aug_out_fp)

class DurUtil:
    def __init__(self, hparam):
        with open(jpath(os.path.dirname(__file__),'google_map_dur_.sh')) as f:
            cmd = f.read()
        self.cmd = cmd.replace('[MAP_KEY]', hparam['google_map_key'])

        self.alias = {}
        self.alias_fp = hparam['data_util_fp']
        if os.path.exists(self.alias_fp):
            self.alias = read_json(self.alias_fp)

    def save_alias(self):
        save_json(self.alias, self.alias_fp)

    def compute_dur(self, loc1, loc2):
        
        dur_gotten = False
        while dur_gotten == False:
            try:
                cmd = self.cmd.replace('[ORIG]', loc1).replace('[DEST]', loc2)
                completed_process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                res = completed_process.stdout
                assert 'routes' in res
                dur_gotten = True
            except:
                # print(loc1, loc2)
                if loc1 in self.alias:
                    loc1 = self.alias[loc1]
                else:
                    print('What is the postcode of \n{} ? \nAnswer in format XXXXXX'.format(loc1))
                    t = input('> ')
                    t = '{}, Singapore'.format(t)
                    self.alias[loc1] = t
                    loc1 = t
        res = json.loads(res)
        return res
        

def parse_time(time_str):
    t = time_str.strip().split(' ')
    if len(t) <=2:
        h = 0
        m = t[0]
    else:
        h = t[0]
        m = t[2]
    return int(h), int(m)

if __name__ == '__main__':
    main()
