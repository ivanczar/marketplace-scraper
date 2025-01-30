import os
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader


class MatchedListings:
    TEMPLATES_DIRECTORY_PATH = os.path.dirname(__file__), "..", "templates"
    TEMPLATE_FILE_NAME = "matched_listings.html"

    def __init__(self):
        self.listings: List[Dict[str, str]] = []

    def add_listing(self, title: str, price: int, img: str) -> None:
        listing = dict(title=title, price=price, img=img)
        self.listings.append(listing)

    def get_formatted_content(self) -> str:
        return self.generate_html()

    def get_formatted_subject(self) -> str:
        count = self.get_listing_count()
        return f"{count} listings found!"

    def get_listing_count(self) -> int:
        return len(self.listings)

    def generate_html(self) -> str:
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIRECTORY_PATH))
        template = env.get_template(self.TEMPLATE_FILE_NAME)
        html_content = template.render(listings=self.listings)

        return html_content
