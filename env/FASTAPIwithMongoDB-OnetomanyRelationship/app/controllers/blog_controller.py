# app/controllers/blog_controller.py

from bson import ObjectId
from app.database.mongodb import db

def create_blog(blog):
    blog_id = db.blogs.insert_one(blog).inserted_id
    blog._id = blog_id
    return blog

def get_blog(blog_id):
    return db.blogs.find_one({"_id": ObjectId(blog_id)})

def get_all_blogs():
    return list(db.blogs.find())


def update_blog(blog_id, updated_blog):
    db.blogs.update_one({"_id": ObjectId(blog_id)}, {"$set": updated_blog})
    return get_blog(blog_id)

def delete_blog(blog_id):
    db.blogs.delete_one({"_id": ObjectId(blog_id)})


def get_all_blogs_all():
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


