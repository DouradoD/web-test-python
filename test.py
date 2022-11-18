class Pages:

    def __int__(self):
        self._pages = None
        self._load_pages()

    def _load_pages(self):
        self._pages = 'test'
        print(self._pages)
        return self._pages


a = Pages()
a._load_pages()
