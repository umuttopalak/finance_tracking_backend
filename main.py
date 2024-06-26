import os
from flask import Flask, request, jsonify, abort
from pydantic import ValidationError
from models import FinancialItem, Category, FinancalItemType
from datetime import datetime
from flask_cors import CORS
from database import read_from_firebase, save_to_firebase
from dotenv import load_dotenv
from shortuuid import uuid
import json

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/categories/", methods=["POST"])      
def create_category():
    data = request.get_json()
    data['id'] = uuid()
    category = Category(**data)
    save_to_firebase(category.to_dict(), f"categories/{category.id}")

    return category.to_dict() , 201

@app.route("/categories/", methods=["GET"])
def get_categories():
    categories_data = read_from_firebase("categories")
    categories_list = [Category(**cat_data).to_dict() for cat_id, cat_data in categories_data.items()]
    return jsonify({"categories":categories_list}), 200

@app.route("/categories/<category_id>", methods=["GET"])
def get_category(category_id):
    category_data = read_from_firebase(f"categories/{category_id}")
    if category_data:
        category = Category(**category_data)
        return jsonify({"category":category.to_dict()}), 200
    return jsonify(),404

@app.route("/financial_items/", methods=["POST"])
def create_financial_item():
    try:
        data = request.get_json()
        data['id'] = uuid()
        item = FinancialItem(**data)
        save_to_firebase(item.to_dict(), f"financial_items/{item.id}")
    
    except ValidationError as e:
        return jsonify(e.errors()), 400

    return jsonify(item.to_dict()), 201

@app.route("/financial_items/", methods=["GET"])
def get_financial_items():
    items = read_from_firebase("financial_items")
    items_list = [FinancialItem(**item_data).to_dict() for item_id, item_data in items.items()]
    return jsonify({"items":items_list}), 200

@app.route("/financial_items/<item_id>", methods=["GET"])
def get_financial_item(item_id):
    item_data = read_from_firebase(f"financial_items/{item_id}")
    if item_data:
        item = FinancialItem(**item_data)
        return jsonify(item.to_dict()), 200
    return jsonify(), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
