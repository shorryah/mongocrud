from pydantic import BaseModel, Field
from datetime import datetime

#representation of a single contact
class Contact(BaseModel):
    name: str
    number: str
    email: str
    address: str
    
    #default timestamp given of when a contact is created and updated respectively
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)



