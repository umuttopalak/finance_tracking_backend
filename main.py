from fastapi import FastAPI, HTTPException
from typing import List
from models import FinancialItem, Category
from datetime import datetime
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request

flask_app = Flask(__name__)


app = FastAPI()

items = []
categories = []
item_id_counter = 1
category_id_counter = 1

@app.post("/categories/", response_model=Category)
def create_category(category: Category):
    global category_id_counter
    category.id = category_id_counter
    category_id_counter += 1
    categories.append(category)
    return category

@app.get("/categories/", response_model=List[Category])
def get_categories():
    return categories

@app.post("/financial_items/", response_model=FinancialItem)
def create_financial_item(item: FinancialItem):
    global item_id_counter
    item.id = item_id_counter
    item_id_counter += 1
    items.append(item)
    return item

@app.get("/financial_items/", response_model=List[FinancialItem])
def get_financial_items():
    return items

@app.get("/financial_items/{item_id}", response_model=FinancialItem)
def get_financial_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Financial item not found")

@app.get("/v2")
def read_main():
    return {"message": "Hello World"}

@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {(name)} from Flask!"


app.mount("/v1", WSGIMiddleware(flask_app))