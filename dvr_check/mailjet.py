from mailjet_rest import Client as _Client

class EmailError(Exception):
    """"""

class Recipient(object):
    email: str
    name: str

    def __init__(self, email, name = "") -> None:
        self.email = email
        self.name = name

class Client(object):
    username: str
    password: str

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self._client = _Client(auth=(username, password), version='v3.1')

    def send(self, address_from: Recipient, address_to: list[Recipient], subject: str, body_html: str = "", body_text=""): 
        data = {
            'Messages': [
                {
                    "From": {
                            "Email": address_from.email,
                            "Name": address_from.name,
                    },
                    "To": [ { "Email": recipient.email, "Name": recipient.name } for recipient in address_to],
                    "Subject": subject,
                    "TextPart": body_text,
                    "HTMLPart": body_html,
                }
            ]
        }
        result = self._client.send.create(data=data)
        
        if result.status_code != 200:
            raise EmailError(result.json())

        return result.json()
