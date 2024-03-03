import os
import hashlib
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import MongoClient
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure CORS
CORS(app, origins="http://localhost:5173",supports_credentials=True)

# Configure Flask JWT
jwt = JWTManager(app)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

# Configure MongoDB
MONGO_URL = os.environ.get("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["medbot"]
users_collection = db["users"]

@app.route("/signup", methods=["POST"])
def register():
    new_user = request.get_json()  # store the json body request
    # Hash the password
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    # Check if the username or email already exists
    existing_user = users_collection.find_one({"$or": [{"username": new_user["username"]}, {"email": new_user["email"]}]})
    if not existing_user:
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username or Email already exists'}), 409
    

@app.route("/login", methods=["POST"])    
def login():
    login_details = request.get_json()
    # Check if the login information is provided
    if 'email' not in login_details or 'password' not in login_details:
        return jsonify({'msg': 'Invalid login details'}), 400
    
    # Query the database based on email
    user_from_db = users_collection.find_one({'email': login_details['email']})
    
    if user_from_db:
        encrypted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrypted_password == user_from_db['password']:
            access_token = create_access_token(identity=user_from_db['email'])
            return jsonify(access_token=access_token,msg='Login successful'), 200

    return jsonify({'msg': 'The email or password is incorrect'}), 401


@app.route("/",methods=["POST"])
@jwt_required
def profile():
    current_user = get_jwt_identity()
    user_from_db = users_collection.find_one({'username':current_user})
    if user_from_db:
        del user_from_db['id'], user_from_db['password']
        return jsonify({'profile' : user_from_db}), 200
    else:
        return jsonify({'msg': 'profile not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
