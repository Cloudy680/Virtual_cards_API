from pydantic import BaseModel
from datetime import date


class Card(BaseModel):
    number : str
    carrier_name : str
    establishment_date : date
    expires_date : date
    payment_system : str

class Card_in_DB(Card):
    cvv : int