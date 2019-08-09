import json
import pycountry
from typing import List


class Prediction:
    """
    This class should be what you receive,
    may need to add more functionality
    """

    def __init__(self, seen=List[str]):
        if seen:
            self.predicted = None
        else:
            self.predicted = max(set(seen), key=seen.count)
        self.data = seen

    def get_confidence(self) -> float:
        """
        approximate counfidence of this prediction
        :return: a number between 0 and 1 of how confident we are of this prediction
        """
        return (self.data.count(self.predicted) / len(self.data)) ** 2

    def get_country(self):
        '''
        In theory this should return a pycountry country
        :return: country
        '''
        return pycountry.countries.get(alpha_2=self.predicted)

    def __str__(self):
        return "<Prediction of {} with a {} percent confidence>".format(str(self.get_country()),
                                                                        str(self.get_confidence()))


class CountryNames:
    def __init__(self, namefile="webpage/data/data_dump/informalnaming.json"):
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

    def get_nicknames(self) -> list[str]:
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
