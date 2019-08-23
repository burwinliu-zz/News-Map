import json
from statistics import mode, StatisticsError
from typing import List, Tuple

import pycountry


class Prediction:
    """
    This class should be what you receive,
    may need to add more functionality
    """

    def __init__(self, seen=List[str]):
        try:
            self.predicted = (mode(seen) if seen else None)
            self.warning = False
        except StatisticsError:
            self.predicted = seen[0]
            self.warning = True
        self.data = seen

    def get_confidence(self) -> float:
        """
        approximate counfidence of this prediction
        :return: a number between 0 and 1 of how confident we are of this prediction
        """
        if self.warning:
            return 0.0
        return (self.data.count(self.predicted) / len(self.data)) ** 2 if self.data else float(0)

    def get_country(self):
        '''
        In theory this should return a pycountry country
        :return: country
        '''
        return pycountry.countries.get(alpha_2=self.predicted) if self.predicted is not None else None

    def get_color(self) -> Tuple[int, int, int]:
        def lcg(modulus, a, c, seed):
            while True:
                seed = (a * seed + c) % modulus
                yield seed

        try:
            rand = lcg(2 ** 31, 1103515245, 12345 * len(self.data), self.get_country()["numberic"])
        except Exception:
            return 0, 0, 0
        return rand.__next__(), rand.__next__(), rand.__next__()

    def __str__(self):
        return "<Prediction of {} with a {} percent confidence>".format(str(self.get_country()),
                                                                        str(self.get_confidence()))


class CountryNames:
    def __init__(self, namefile="webpage/server/data/data_dump/informalnaming.json"):
        with open(namefile, 'r+') as fp:
            self.internal = json.load(fp)
        if not self.internal:
            raise Exception("oh dear")

    def predict(self, on: str) -> Prediction:
        result = []
        for country in self.internal:
            for nickname in country['nicknames']:
                if on.find(nickname) >= 0:
                    result.append(country["iso3166_code"])
        return Prediction(result)

    def get_countries(self) -> List[str]:
        return [country["country_name"] for country in self.internal]

    def get_nicknames(self) -> List[str]:
        """
        I hope this list comprehension works
        :return:
        """
        return [nickname for country in self.internal for nickname in country['nicknames']]

    def stats(self) -> str:
        countries = 0
        nicknames = 0
        for country in self.internal:
            countries += 1
            nicknames += len(country['nicknames'])
        return "We have {} countries and {} names for them".format(str(countries), str(nicknames))

    def __str__(self):
        return "this is a class to guess countries. Fuck off now. If you wanted stats, call that method"
