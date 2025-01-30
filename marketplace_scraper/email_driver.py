import yagmail
from marketplace_scraper.matched_listings import MatchedListings


class Email:
    def __init__(self, email: str, pswd: str):
        self.client = yagmail.SMTP(email, pswd)

    def send(self, data: MatchedListings, to_email: str) -> None:
        print("Sending email...")

        formatted_subject = data.get_formatted_subject()
        formatted_content = data.get_formatted_content()

        self.client.send(to_email, formatted_subject, formatted_content)
        print("Email sent!")
