from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.models.blog import Blog
from app.models.comment import Comment
from app.models.reply import Reply
from app.database.mongodb import db
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/blogs/search/")
async def search_blogs(keyword: str):
    # Perform a case-insensitive search using a regular expression
    query = {"text": {"$regex": f".*{keyword}.*", "$options": "i"}}
    blogs = list(db.blogs.find(query, {"_id": 0}))
    return blogs


#server side pagination
# @router.get("/blogs", response_model=List[dict])
# async def get_all_blogs(page: int = Query(1, ge=1), limit: int = Query(10, le=100)):
#     # Calculate the number of blogs to skip based on the page and limit
#     skip = (page - 1) * limit

#     # Fetch blogs with pagination from the database in descending order of their creation timestamp
#     blogs = list(db.blogs.find().sort("_id", -1).skip(skip).limit(limit))

#     # Convert the ObjectId to string representation for each blog
#     for blog in blogs:
#         blog["_id"] = str(blog["_id"])

#         # Fetch comments for the current blog using its "_id" in descending order of their creation timestamp
#         blog_comments = list(db.comments.find({"blog_id": blog["_id"]}).sort("_id", -1))
#         for comment in blog_comments:
#             comment["_id"] = str(comment["_id"])

#             # Fetch replies for the current comment using its "_id" in descending order of their creation timestamp
#             comment_replies = list(db.replies.find({"comment_id": comment["_id"]}).sort("_id", -1))
#             for reply in comment_replies:
#                 reply["_id"] = str(reply["_id"])

#             # Add replies to the comment
#             comment["replies"] = comment_replies

#         # Add comments to the blog
#         blog["comments"] = blog_comments

#     # Return the list of blogs with comments and replies included
#     return blogs


@router.get("/blogs", response_model=List[dict])
async def get_all_blogs():
    # Fetch all blogs from the database in descending order of their creation timestamp
    blogs = list(db.blogs.find().sort("_id", -1))

    # Convert the ObjectId to string representation for each blog
    for blog in blogs:
        blog["_id"] = str(blog["_id"])

        # Fetch comments for the current blog using its "_id" in descending order of their creation timestamp
        blog_comments = list(db.comments.find({"blog_id": blog["_id"]}).sort("_id", -1))
        for comment in blog_comments:
            comment["_id"] = str(comment["_id"])

            # Fetch replies for the current comment using its "_id" in descending order of their creation timestamp
            comment_replies = list(db.replies.find({"comment_id": comment["_id"]}).sort("_id", -1))
            for reply in comment_replies:
                reply["_id"] = str(reply["_id"])

            # Add replies to the comment
            comment["replies"] = comment_replies

        # Add comments to the blog
        blog["comments"] = blog_comments

    # Return the list of blogs with comments and replies included
    return blogs


# @router.get("/blogs", response_model=List[dict])
# async def get_all_blogs():
#     # Fetch all blogs from the database
#     blogs = list(db.blogs.find())

#     # Convert the ObjectId to string representation for each blog
#     for blog in blogs:
#         blog["_id"] = str(blog["_id"])

#         # Fetch comments for the current blog using its "_id"
#         blog_comments = list(db.comments.find({"blog_id": blog["_id"]}))
#         for comment in blog_comments:
#             comment["_id"] = str(comment["_id"])

#             # Fetch replies for the current comment using its "_id"
#             comment_replies = list(db.replies.find({"comment_id": comment["_id"]}))
#             for reply in comment_replies:
#                 reply["_id"] = str(reply["_id"])

#             # Add replies to the comment
#             comment["replies"] = comment_replies

#         # Add comments to the blog
#         blog["comments"] = blog_comments

#     # Return the list of blogs with comments and replies included
#     return blogs


# @router.get("/blogs", response_model=List[dict])  # Use List[dict] to specify the response as a list of dictionaries
# async def get_all_blogs():
#     blogs = list(db.blogs.find())  
#     for blog in blogs:
#         blog["_id"] = str(blog["_id"])
#     return blogs

# @router.get("/blogs", response_model=List[Blog])  # Use List[Blog] to specify the response as a list of Blog models
# async def get_all_blogs():
#     blogs = list(db.blogs.find())  # Retrieve all blog entries from the database
#     return blogs


@router.post("/blogs/", response_model=Blog)
async def create_blog(blog: Blog):
    new_blog = blog.dict()
    # Save the new_blog to MongoDB using db collection
    inserted_blog = db.blogs.insert_one(new_blog)
    new_blog["_id"] = inserted_blog.inserted_id
    return new_blog

@router.get("/blogs/{blog_id}", response_model=Blog)
async def get_blog(blog_id: str):  # Use str as parameter type
    # Convert the blog_id string back to ObjectId before querying the database
    object_id = ObjectId(blog_id)
    blog = db.blogs.find_one({"_id": object_id})
    if blog:
        return blog
    raise HTTPException(status_code=404, detail="Blog not found")


@router.put("/blogs/{blog_id}", response_model=Blog)
async def update_blog(blog_id: str, blog: Blog):
    # Convert the blog_id string to ObjectId
    object_id = ObjectId(blog_id)
    
    existing_blog = db.blogs.find_one({"_id": object_id})
    if existing_blog:
        updated_blog = blog.dict()
        # Do not update the "_id" field
        updated_blog.pop("id", None)
        
        db.blogs.update_one({"_id": object_id}, {"$set": updated_blog})
        return {**existing_blog, **updated_blog}
    
    raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/blogs/{blog_id}", response_model=Blog)
async def delete_blog(blog_id: str):
    # Convert the blog_id string to ObjectId
    object_id = ObjectId(blog_id)
    
    existing_blog = db.blogs.find_one({"_id": object_id})
    if existing_blog:
        db.blogs.delete_one({"_id": object_id})
        return existing_blog
    
    raise HTTPException(status_code=404, detail="Blog not found")