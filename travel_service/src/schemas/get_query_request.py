class GetQueryRequest:
    def __init__(self, page: int = 1, limit: int = 10, search: str | None = None):
        self.page = page
        self.limit = limit
        self.search = search
