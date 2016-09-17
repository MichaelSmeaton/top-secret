from abc import ABC, abstractmethod, ABCMeta
from src.view import CmdView
from collections import OrderedDict
import pickle


class Controller(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, model):
        self._model = model
        self._view = []

    @abstractmethod
    def go(self):
        return "Start your engines!"


class WebScrapingController(Controller):
    def __init__(self, model):
        super(WebScrapingController, self).__init__(model)
        self._view = CmdView(self)
        self._data = []
        self._links = []
        self._container = {
            'album': [],
            'artist': [],
            'ranking': [],
            'image': [],
            'price': []
        }
        self._url = "http://www.apple.com/nz/itunes/charts/albums/"
        self.load_pickle_data()

    def go(self):
        self._view.cmdloop()

    def get_url(self):
        return self._url

    def get_correct_url(self, url):
        return self._model.is_correct(url)

    def get_connection(self, url):
        return self._model.is_connected(url)

    def set_to_input(self, url):
        self._url = self.get_correct_url(url)
        return True

    def get_data(self):
        if self.get_connection(self._url):
            self._data = self._model.fetch(self._url)
            self._container['album'] = self._model.extract(self._data, "album")
            self._container['artist'] = self._model.extract(self._data,
                                                            "artist")
            self._container['ranking'] = self._model.extract(self._data,
                                                             "ranking")
            self._container['image'] = self._model.extract(self._data, "image")
            self._links = self._model.extract(self._data, "link")
            for link in self._links:
                self._data = self._model.fetch_by_keyword(link, "class",
                                                          "price")
                self._container['price'].append(self._model.extract(self._data,
                                                                    "price"))
            return True

    def get_container(self, index):
        container = OrderedDict(sorted(self._container.items()))
        ls = []
        for i, key in enumerate(container.keys()):
            ls.append(key.upper() + ": ")
            ls.append(container[key][int(index)])
        return ls

    def save_pickle_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self._container, f)

    def load_pickle_data(self):
        try:
            with open('data.pickle', 'rb') as f:
                self._container = pickle.load(f)
        except FileNotFoundError:
            print("Existing data not found.")
            return
