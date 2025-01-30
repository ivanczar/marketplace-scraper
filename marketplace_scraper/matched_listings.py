from typing import List, Dict

class MatchedListings:
    def __init__(self):
        self.listings: List[Dict[str, str]] = []

    def add_listing(self, title: str, price: int, img: str) -> None:
        listing = dict(title=title, price=price, img=img)
        self.listings.append(listing)

    def get_formatted_subject(self) -> str:
        count = self.get_listing_count()
        return f"{count} listings found!"

    def get_listing_count(self) -> int:
        return len(self.listings)
