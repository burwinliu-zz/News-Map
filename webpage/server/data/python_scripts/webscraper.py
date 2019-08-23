from webpage.server.webscraping import Headlines
from .data import store_articles
from psycopg2 import DataError

def make_legal(headline: str) -> str:
    '''
    There is the idea of making this leagal for the input
    :param headline:
    :return:
    '''
    headline = headline.replace("'", "''")
    return headline


class DataLoader(Headlines):
    def __init__(self, search_space='world', batch_size=10):
        if search_space == 'world':
            super().__init__()
        elif search_space == 'US':
            super().__init__("https://news.google.com/?hl=en-US&gl=US&ceid=US:en")
        self.datadump = self.gen_samples(batch_size=batch_size, predict_country=True)

    def __str__(self):
        return "<Dataloader with Headline>" + super.__str__()

    def dump_batch(self) -> None:
        """
        This dumps a batch into the store article function
        :return: NOne
        """
        batch = self.datadump.__next__()
        urls = []
        headlines = []
        isocodes = []
        for entry in batch:
            headlines.append(make_legal(str(entry['soup'].head.title.string))[:75])
            urls.append(str(entry['full']))
            country = entry['country'].get_country()
            if country is None:
                isocodes.append(0)
            else:
                isocodes.append(int(country.numeric))
            try:
                store_articles(urls=urls, headlines=headlines, iso_codes=isocodes)
            except SyntaxError as e:
                print(e)
            except DataError as e1:
                print(str(e1)+"sigh fuck this")
            urls = []
            headlines = []
            isocodes = []
