import yagmail
from matched_listings import MatchedListings


class Email:
    def __init__(self, email: str, pswd: str):
        self.client = yagmail.SMTP(email, pswd)

    def send(self, data: MatchedListings, toEmail: str) -> None:
        print("Sending email...")

        formattedSubject = data.getFormattedSubject()
        formattedContent = data.getFormattedContent()

        self.client.send(toEmail, formattedSubject, formattedContent)
        print("Email sent!")
