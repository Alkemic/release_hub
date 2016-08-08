class BaseScrapper:
    @property
    def project_name(self):
        raise NotImplementedError

    def register(self):
        raise NotImplementedError

    def initial(self):
        raise NotImplementedError

    def recent(self):
        raise NotImplementedError
