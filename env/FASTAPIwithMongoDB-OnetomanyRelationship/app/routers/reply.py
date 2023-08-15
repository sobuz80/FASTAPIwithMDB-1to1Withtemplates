from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.reply import Reply
from app.database.mongodb import db
from bson import ObjectId
router = APIRouter()

@router.post("/replies/", response_model=Reply)
async def create_reply(reply: Reply):
    new_reply = reply.dict()
    # Save the new_reply to MongoDB using db collection
    inserted_reply = db.replies.insert_one(new_reply)
    new_reply["_id"] = inserted_reply.inserted_id
    return new_reply

@router.get("/replies/{reply_id}", response_model=Reply)
async def get_reply(reply_id: str):
    # Convert the reply_id string to ObjectId
    reply_object_id = ObjectId(reply_id)

    reply = db.replies.find_one({"_id": reply_object_id})
    if reply:
        return reply
    raise HTTPException(status_code=404, detail="Reply not found")

@router.put("/replies/{reply_id}", response_model=Reply)
async def update_reply(reply_id: str, reply: Reply):
    # Convert the reply_id string to ObjectId
    reply_object_id = ObjectId(reply_id)

    existing_reply = db.replies.find_one({"_id": reply_object_id})
    if existing_reply:
        updated_reply = reply.dict()
        # Do not update the "_id" field
        updated_reply.pop("id", None)
        
        db.replies.update_one({"_id": reply_object_id}, {"$set": updated_reply})
        return {**existing_reply, **updated_reply}
    
    raise HTTPException(status_code=404, detail="Reply not found")


@router.delete("/replies/{reply_id}", response_model=Reply)
async def delete_reply(reply_id: str):
    # Convert the reply_id string to ObjectId
    reply_object_id = ObjectId(reply_id)

    existing_reply = db.replies.find_one({"_id": reply_object_id})
    if existing_reply:
        db.replies.delete_one({"_id": reply_object_id})
        return existing_reply
    
    raise HTTPException(status_code=404, detail="Reply not found")

