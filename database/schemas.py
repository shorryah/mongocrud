# a contact from the database is taken and important information such as name and phone number is returned
def individual_data(contact):
    return {
        "id": str(contact["_id"]), #mongodb id converted into a string
        "name": contact["name"],
        "phone number": contact["number"],
        "email": contact["email"],
        "address": contact["address"]
    }

#returns all the contacts from the database
def all_contacts(contacts):
    return [individual_data(contact) for contact in contacts]