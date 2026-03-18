# 🍕 FastAPI Food Delivery App

##  Project Overview

This project is a backend application built using FastAPI. It simulates a real-world food delivery system where users can browse menu items, add items to a cart, place orders, and perform various operations like search, sorting, and pagination.

---

## 🚀 Features

### 🔹 Menu Management

* View all menu items
* Get item by ID
* Menu summary (available/unavailable items)
* Add new menu item
* Update menu item
* Delete menu item

### 🔹 Orders

* Place new order
* View all orders
* Search orders by customer name
* Sort orders by total price

### 🔹 Cart System

* Add items to cart
* Update item quantity
* Remove items from cart
* View cart with total price

### 🔹 Checkout Workflow

* Convert cart into orders
* Generate multiple orders
* Clear cart after checkout

### 🔹 Advanced Features

* Search menu items (keyword based)
* Filter menu (category, price, availability)
* Sort menu items
* Pagination support
* Combined browsing API (search + sort + pagination)

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run server

```bash
uvicorn main:app --reload
```

### 3️⃣ Open Swagger UI

👉 http://127.0.0.1:8000/docs

---

## 📸 Screenshots

All API outputs and testing screenshots are available in the `screenshots` folder.

---

## 🎯 Key Concepts Covered

* FAST API development
* Pydantic validation
* CRUD operations
* Helper functions
* Multi-step workflows (Cart → Checkout)
* Search, Sorting, Pagination
* API testing using Swagger UI

---

##  Acknowledgement

This project was completed as part of the FastAPI Internship at Innomatics Research Labs.
