from fastapi import FastAPI, HTTPException
from datetime import datetime
from configurations import collection
from database.schemas import all_contacts
from database.models import Contact
from bson.objectid import ObjectId

app = FastAPI() #creates Fast API application

#Get all the contact
#retrieves data from the collection and returns it as a list
@app.get("/") 
async def get_all_contacts():
    data = collection.find() 
    return all_contacts(data)

#Create new contact
@app.post("/")
async def create_contact(new_contact: Contact):
    try:
        resp = collection.insert_one(dict(new_contact)) #converts the pydantic model to a dictionary and adds it as a new contact on MongoDB
        return {"status_code": 200, "id":str(resp.inserted_id)} #message returned if successful
    
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occurred {e}") #message returned if an error has occurred

#Update a contact based on the contact ID
@app.put("/{contact_id}")
async def update_contact(contact_id: str, updated_contact: Contact):
    try:
        updated_contact.updated_at = int(datetime.timestamp(datetime.now())) #updated_at is updated to the correct time
        result = collection.update_one({"_id": ObjectId(contact_id)}, {"$set": dict(updated_contact)}) #updates the contact whose ID it matches and sets the new data
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found") # 404 Error is given if ID given does not match with any ID in the database
        return {"status_code": 200, "message": "Contact updated successfully"} # message returned if successful
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}") #message returned if an error has occurred

#Remove a contact
@app.delete("/{contact_id}")
async def delete_contact(contact_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(contact_id)}) #delete ID of contact that matches the given ID
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found") # if no contact is deleted, contact is not found and hence a 404 error is given
        return {"status_code": 200, "message": "Contact deleted"} #message returned if successful
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}") #message returned if an error has occurred