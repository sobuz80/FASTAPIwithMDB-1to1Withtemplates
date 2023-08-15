from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.comment import Comment
from app.database.mongodb import db
from bson import ObjectId
router = APIRouter()

@router.post("/comments/", response_model=Comment)
async def create_comment(comment: Comment):
    new_comment = comment.dict()
    # Save the new_comment to MongoDB using db collection
    inserted_comment = db.comments.insert_one(new_comment)
    new_comment["_id"] = inserted_comment.inserted_id
    return new_comment

@router.get("/comments/{comment_id}", response_model=Comment)
async def get_comment(comment_id: str):
    # Convert the comment_id string to ObjectId
    comment_object_id = ObjectId(comment_id)

    comment = db.comments.find_one({"_id": comment_object_id})
    if comment:
        return comment
    raise HTTPException(status_code=404, detail="Comment not found")

@router.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: str, comment: Comment):
    # Convert the comment_id string to ObjectId
    comment_object_id = ObjectId(comment_id)

    existing_comment = db.comments.find_one({"_id": comment_object_id})
    if existing_comment:
        updated_comment = comment.dict()
        # Do not update the "_id" field
        updated_comment.pop("id", None)
        
        db.comments.update_one({"_id": comment_object_id}, {"$set": updated_comment})
        return {**existing_comment, **updated_comment}
    
    raise HTTPException(status_code=404, detail="Comment not found")

@router.delete("/comments/{comment_id}", response_model=Comment)
async def delete_comment(comment_id: str):
    # Convert the comment_id string to ObjectId
    comment_object_id = ObjectId(comment_id)

    existing_comment = db.comments.find_one({"_id": comment_object_id})
    if existing_comment:
        db.comments.delete_one({"_id": comment_object_id})
        return existing_comment
    
    raise HTTPException(status_code=404, detail="Comment not found")