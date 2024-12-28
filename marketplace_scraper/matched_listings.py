class MatchedListings:
    def __init__(self):
        self.count: int = 0
        self.titles: list = []
        self.prices: list = []

    def getFormattedContent(self) -> str:
        return f"●{self.titles[0]} matches●"

    def getFormattedSubject(self) -> str:
        return f"●{self.count} matches●"
