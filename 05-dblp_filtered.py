from tqdm import tqdm
import concurrent.futures
import json
import pickle
import xmltodict


class DblpFilter:
    def __init__(self, faculties_dic, dblp):
        self.faculties_dic = faculties_dic
        self.dblp = dblp

    def get_res(self):
        fac_li = []
        for fac_dic in self.faculties_dic.values():
            fac_li.extend(list(fac_dic.keys()))
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            res_tup_li = list(
                tqdm(executor.map(self.mp_dblp_filter, fac_li),
                     total=len(fac_li), desc='filtering: '))

        self.res_dic = dict(res_tup_li)
        with open('dblp_filtered.pickle', 'wb') as f:
            pickle.dump(self.res_dic, f)

    def mp_dblp_filter(self, fac):
        _dic = {}
        for k, li in self.dblp.items():
            _dic[k] = []
            for dic in li:
                if 'author' in dic.keys():
                    author = dic['author']
                    if fac in author:
                        _dic[k].append(dic)
        return fac, _dic


if __name__ == "__main__":
    with open('faculties_by_interests.json', 'r') as f:
        faculties_dic = json.load(f)
    with open('../CSrankings/dblp.xml', 'r', encoding="ISO-8859-1") as f:
        dblp = xmltodict.parse(f.read())
    db_filter = DblpFilter(faculties_dic, dblp['dblp'])
    db_filter.get_res()