from pymongo import MongoClient
from urllib.parse import quote_plus

# Encode the username and password
username = 'shubhambhayaje913'
password = 'n8GGzx5C0KJ35vDG'
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Construct the connection URI with encoded username and password
connection_uri = f'mongodb+srv://{encoded_username}:{encoded_password}@cluster0.pbpp7vk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(connection_uri)

# The rest of your code remains the same
db = client['create_custom_commands']
collection = db['create_custom_commandss']
document = {"command": "whatapp", "path": "C:\Friday\engine\Custom_Commands\discord.py"}
insert_doc = collection.insert_one(document)
print(f"Inserted Doc id: {insert_doc.inserted_id}")

client.close()
