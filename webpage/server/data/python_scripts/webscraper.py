from webpage.server.webscraping import Headlines
from .data import store_articles


class DataLoader(Headlines):
    def __init__(self, type='world', batch_size=10):
        if type == 'world':
            super().__init__()
        elif type == 'US':
            super().__init__("https://news.google.com/?hl=en-US&gl=US&ceid=US:en")
        self.datadump = self.gen_samples(batch_size=batch_size, predict_country=True)

    def __str__(self):
        return "<Dataloader with Headline>" + super.__str__()

    def dump_batch(self):
        batch = self.datadump.__next__()
        urls = []
        headlines = []
        isocodes = []
        for entry in batch:
            headlines.append(str(entry['soup'].head.title))
            urls.append(str(entry['full']))
            try:
                isocodes.append(int(entry['country'].get_country().numeric))
            except Exception as e:
                print(e)
                isocodes.append(0)
        store_articles(urls=urls, headlines=headlines, iso_codes=isocodes)