from pymongo import MongoClient

# Replace 'YOUR_MONGODB_URI' with your actual MongoDB Atlas URI
MONGODB_URI = "mongodb+srv://11335220:11335220@cluster0.ojobzbu.mongodb.net/Todo?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)
db = client.get_database("Todo")  # Replace 'my_database' with your preferred database name


