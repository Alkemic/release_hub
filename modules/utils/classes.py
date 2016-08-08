class BaseScrapper:
    def register(self):
        raise NotImplementedError

    def initial(self):
        raise NotImplementedError

    def recent(self):
        raise NotImplementedError
