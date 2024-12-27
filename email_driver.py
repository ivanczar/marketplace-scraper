import yagmail

class Email:

    def __init__(self, email, pswd):
        self.client = yagmail.SMTP(email, pswd);

    def send(self, data, toEmail):
        print("Sending email...")

        matchCount = data.count;
        listings = data.titles[0];
        
        self.client.send(toEmail, f'●{matchCount} matches●', listings)
        print("Email sent!")
