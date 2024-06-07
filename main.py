from flask import Flask, request, jsonify, abort
from pydantic import ValidationError
from models import FinancialItem, Category
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


items = []
categories = []
item_id_counter = 1
category_id_counter = 1

@app.route("/categories/", methods=["POST"])
def create_category():
    global category_id_counter
    try:
        data = request.get_json()
        category = Category(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category.id = category_id_counter
    category_id_counter += 1
    categories.append(category)
    return jsonify(category.dict()), 201

@app.route("/categories/", methods=["GET"])
def get_categories():
    return jsonify([category.dict() for category in categories])

@app.route("/financial_items/", methods=["POST"])
def create_financial_item():
    global item_id_counter
    try:
        data = request.get_json()
        item = FinancialItem(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    item.id = item_id_counter
    item_id_counter += 1
    items.append(item)
    return jsonify(item.dict()), 201

@app.route("/financial_items/", methods=["GET"])
def get_financial_items():
    return jsonify([item.dict() for item in items])

@app.route("/financial_items/<int:item_id>", methods=["GET"])
def get_financial_item(item_id):
    for item in items:
        if item.id == item_id:
            return jsonify(item.dict())
    abort(404, description="Financial item not found")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
