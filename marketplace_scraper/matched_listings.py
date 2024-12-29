from typing import List, Dict
from jinja2 import Environment, FileSystemLoader
import os


class MatchedListings:
    TEMPLATES_DIRECTORY_PATH = os.path.dirname(__file__), "..", "templates"
    TEMPLATE_FILE_NAME = "matched_listings.html"

    def __init__(self):
        self.listings: List[Dict[str, str]] = []

    def addListing(self, title: str, price: int, img: str) -> None:
        listing = dict(title=title, price=price, img=img)
        self.listings.append(listing)

    def getFormattedContent(self) -> str:
        return self.generateHtml()

    def getFormattedSubject(self) -> str:
        count = self.getListingCount()
        return f"{count} listings found!"

    def getListingCount(self) -> int:
        return len(self.listings)

    def generateHtml(self) -> str:
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIRECTORY_PATH))
        template = env.get_template(self.TEMPLATE_FILE_NAME)
        html_content = template.render(listings=self.listings)

        return html_content
