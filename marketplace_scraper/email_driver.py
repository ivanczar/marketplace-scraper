import os
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
import yagmail
from marketplace_scraper.matched_listings import MatchedListings


class Email:
    TEMPLATES_DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), "templates")
    TEMPLATE_FILE_NAME = "matched_listings.html"

    def __init__(self, email: str, pswd: str):
        self.client = yagmail.SMTP(email, pswd)

    def send(self, data: MatchedListings, to_email: str) -> None:
        print("Sending email...")

        formatted_subject = data.get_formatted_subject()
        formatted_content = self.generate_html(data.listings)

        self.client.send(to_email, formatted_subject, formatted_content)
        print("Email sent!")

    def generate_html(self, matched_listings: List[Dict[str, str]]) -> str:
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_DIRECTORY_PATH))
        template = env.get_template(self.TEMPLATE_FILE_NAME)
        html_content = template.render(listings=matched_listings)

        return html_content
