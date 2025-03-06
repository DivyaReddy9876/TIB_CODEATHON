# TIB_CODEATHON
📌 1. Project Introduction
This project is a Flask-based REST API implementing Role-Based Access Control (RBAC).
It manages two main entities:
Organisation – Companies, colleges, or communities.
Employee – Employees working for these organizations.
Security: Uses JWT (JSON Web Token) for authentication.
Database: Stores data in MongoDB.
Permissions:
Role 1: Can Create & Read.
Role 2: Can Create, Read & Update.
Role 3: Can perform full CRUD operations.
📂 2. Project Structure
rbac-flask-app/
├── app.py           # Main Flask application (routes and logic)
├── models.py        # Defines Organisation & Employee models (CRUD)
├── rbac.py          # Implements Role-Based Access Control
├── config.py        # Configuration (MongoDB URI & JWT key)
└── requirements.txt # List of required packages
🔍 3. Core Components
a) Configuration – config.py
Handles application configuration. It defines MongoDB connection and JWT secret key:
class Config:
    MONGO_URI = "mongodb://localhost:27017/mydatabase"
    JWT_SECRET_KEY = "your_secret_key"
b) RBAC Logic – rbac.py
Defines the role_required decorator, which checks if the logged-in user has the required permissions.
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()  # Ensures only authenticated users access routes
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()  # Get user info from token
            role = identity.get("role")
            
            if role != required_role:
                return jsonify({"msg": "Forbidden: You don't have the required role"}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
c) Main Application – app.py
This file brings everything together by handling:

User Authentication
Organisation and Employee APIs
Role-based restrictions
🔐 4. API Endpoints Explanation
a) User Authentication
Allows users to log in and get a JWT token:

users = {
    "user1": {"password": "pass123", "role": "role1"},
    "user2": {"password": "pass123", "role": "role2"},
    "user3": {"password": "pass123", "role": "role3"},
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity={"username": username, "role": users[username]['role']})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401
Flow of Login Process:

User sends username and password.
If valid, generates a JWT token.
This token is required for all protected endpoints.
b) Organisation CRUD Operations
Defines APIs to create, read, update, and delete Organisations.

Create & Read – Only for role2 and above:

class Organisation(Resource):
    @jwt_required()
    @role_required("role2")
    def get(self):
        orgs = mongo.db.organisations.find()
        return jsonify([org for org in orgs])

    @jwt_required()
    @role_required("role2")
    def post(self):
        data = request.get_json()
        org = mongo.db.organisations.insert_one(data)
        return jsonify({"msg": "Organisation Created", "id": str(org.inserted_id)})
Update & Delete – For role3 only:

class OrganisationDetail(Resource):
    def put(self, org_id):
        data = request.get_json()
        mongo.db.organisations.update_one({"_id": ObjectId(org_id)}, {"$set": data})
        return jsonify({"msg": "Organisation updated successfully"})
        
    def delete(self, org_id):
        mongo.db.organisations.delete_one({"_id": ObjectId(org_id)})
        return jsonify({"msg": "Organisation deleted successfully"})
c) Employee CRUD Operations
Create – Restricted to role1 and above.
Read – For role3 only.
class Employee(Resource):
    @jwt_required()
    @role_required("role3")
    def get(self):
        employees = mongo.db.employees.find()
        return jsonify([emp for emp in employees])

    @jwt_required()
    @role_required("role1")
    def post(self):
        data = request.get_json()
        employee = mongo.db.employees.insert_one(data)
        return jsonify({"msg": "Employee Created", "id": str(employee.inserted_id)})
🔁 5. Flow of the Application
User Authentication:
Users log in to receive a JWT token.
Role Verification:
Each route is protected by the role_required decorator.
CRUD Access:
Based on user roles, specific endpoints (Create, Read, Update, Delete) are available.
✅ 6. Testing the Application
Start MongoDB:

mongod --dbpath /path/to/data/db
Run Flask App:

python app.py
a) Login & Get Token

POST http://localhost:5001/login
{
  "username": "user1",
  "password": "pass123"
}
b) Create Organisation

POST http://localhost:5001/organisations
Authorization: Bearer <your_token>

{
  "name": "ABC Corp",
  "location": "Hyderabad"
}
c) Fetch Employees

GET http://localhost:5001/employees
Authorization: Bearer <your_token>
📊 7. Key Features Recap
Secure – Uses JWT for user verification.
RBAC – Manages access levels using role_required.
Flexible CRUD – Handle multiple models (Organisation, Employee).
MongoDB – Scalable and flexible for real-world usage.
Modular Design – Easily extendable for future models.
🚀 8. Conclusion & Future Scope
This project is a scalable Flask application implementing secure RBAC.

Future Enhancements:

Add search functionality for large datasets.
Implement pagination for large records.
Logging & Monitoring for better tracking.
