from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource
from rbac import role_required  # Import the role_required decorator

app = Flask(__name__)
api = Api(app)

# Configure MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
app.config["JWT_SECRET_KEY"] = "b4960709ff21651999d9d87fdd3d8f863c5ab5e59a0862ef"  # Use a secret key for JWT

mongo = PyMongo(app)
jwt = JWTManager(app)

# Dummy users data (for authentication testing)
users = {
    "user1": {"password": "password123", "role": "role1"},
    "user2": {"password": "password123", "role": "role2"},
    "user3": {"password": "password123", "role": "role3"},
}

# Authentication route to issue JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity=username, additional_claims={"role": users[username]['role']})
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401

# Object Models (MongoDB Collection)
class Organisation(Resource):
    @jwt_required()  # Ensure user is authenticated
    @role_required("role2")  # Protect this route for users with role2
    def get(self):
        # Get all organisations from MongoDB
        orgs = mongo.db.organisations.find()
        return jsonify([org for org in orgs])

    @jwt_required()  # Ensure user is authenticated
    @role_required("role2")  # Protect this route for users with role2
    def post(self):
        # Create a new organisation
        data = request.get_json()
        organisation = mongo.db.organisations.insert_one(data)
        return jsonify({"msg": "Organisation Created", "id": str(organisation.inserted_id)})

class Employee(Resource):
    @jwt_required()  # Ensure user is authenticated
    @role_required("role3")  # Protect this route for users with role3
    def get(self):
        # Get all employees from MongoDB
        employees = mongo.db.employees.find()
        return jsonify([emp for emp in employees])

    @jwt_required()  # Ensure user is authenticated
    @role_required("role1")  # Protect this route for users with role1
    def post(self):
        # Create a new employee
        data = request.get_json()
        employee = mongo.db.employees.insert_one(data)
        return jsonify({"msg": "Employee Created", "id": str(employee.inserted_id)})

# Assigning Routes to Resources
api.add_resource(Organisation, '/organisations')
api.add_resource(Employee, '/employees')

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Ensure app runs on port 5001
