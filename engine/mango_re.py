from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection URI
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.pbpp7vk.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database('<dbname>')  # Replace '<dbname>' with your database name
collection = db.get_collection('<collection_name>')  # Replace '<collection_name>' with your collection name


@app.route('/')
def index():
    # Fetch data from MongoDB
    data = list(collection.find({}))  # Retrieve all documents from the collection

    # Pass the data to the HTML template
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
