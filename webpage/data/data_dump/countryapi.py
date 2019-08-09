import json
import pycountry
from typing import List


class Prediction:
    '''
    Should do more in this class this is what you will recieve
    '''
    def __init__(self, seen=List[str]):
        if seen:
            self.predicted = None
        else:
            self.predicted = max(set(seen), key=seen.count)
        self.data = seen
    def get_confidence(self)->float:
        '''
        approximate counfidence of this prediction
        :return:
        '''
        return (self.data.count(self.predicted)/len(self.data))**2
    def get_country(self):
        '''
        In theory this should return a pycountry country
        :return: country
        '''
        return None

class CountryNames:
    def __init__(self):
        with open("webpage/data/data_dump/informalnaming.json", 'r+') as fp:
            self.internal = json.load(fp)

    def gen_prediction(self, on: str) -> Prediction:

        return Prediction([])
