from flask_restful import Resource
from flask import jsonify, request
from bson import ObjectId

# Organisation Resource for handling a list of organisations
class OrganisationList(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self):
        organisations = self.mongo.db.organisations.find()
        return jsonify([org for org in organisations])

    def post(self):
        data = request.get_json()
        organisation = self.mongo.db.organisations.insert_one(data)
        return jsonify({"msg": "Organisation Created", "id": str(organisation.inserted_id)})


# Organisation Detail for handling a single organisation by ID
class OrganisationDetail(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def put(self, org_id):
        data = request.get_json()
        if not ObjectId.is_valid(org_id):
            return jsonify({"msg": "Invalid org_id format"}), 400
        result = self.mongo.db.organisations.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"msg": "Organisation not found"}), 404
        return jsonify({"msg": "Organisation updated successfully"}), 200

    def delete(self, org_id):
        if not ObjectId.is_valid(org_id):
            return jsonify({"msg": "Invalid org_id format"}), 400
        result = self.mongo.db.organisations.delete_one({"_id": ObjectId(org_id)})
        if result.deleted_count == 0:
            return jsonify({"msg": "Organisation not found"}), 404
        return jsonify({"msg": "Organisation deleted successfully"}), 200


# Employee Resource for handling a list of employees
class EmployeeList(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def get(self):
        employees = self.mongo.db.employees.find()
        return jsonify([emp for emp in employees])

    def post(self):
        data = request.get_json()
        employee = self.mongo.db.employees.insert_one(data)
        return jsonify({"msg": "Employee Created", "id": str(employee.inserted_id)})


# Employee Detail for handling a single employee by ID
class EmployeeDetail(Resource):
    def __init__(self, mongo):
        self.mongo = mongo

    def put(self, emp_id):
        data = request.get_json()
        if not ObjectId.is_valid(emp_id):
            return jsonify({"msg": "Invalid emp_id format"}), 400
        result = self.mongo.db.employees.update_one(
            {"_id": ObjectId(emp_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"msg": "Employee not found"}), 404
        return jsonify({"msg": "Employee updated successfully"}), 200

    def delete(self, emp_id):
        if not ObjectId.is_valid(emp_id):
            return jsonify({"msg": "Invalid emp_id format"}), 400
        result = self.mongo.db.employees.delete_one({"_id": ObjectId(emp_id)})
        if result.deleted_count == 0:
            return jsonify({"msg": "Employee not found"}), 404
        return jsonify({"msg": "Employee deleted successfully"}), 200
