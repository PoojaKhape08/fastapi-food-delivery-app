This folder contains all the screenshots of API outputs for the FastAPI Food Delivery Project.

Each screenshot represents a specific question (Q1–Q20) from the project assignment. Since the screenshots show only outputs, this file explains what each question does.

---

## 🔹 Day 1 — Basic GET APIs

**Q1 — Home Route**
Displays a welcome message from the API.

**Q2 — Get Menu**
Returns all food items along with total count.

**Q3 — Get Item by ID**
Fetches a specific item using its ID (valid & invalid cases tested).

**Q4 — Get Orders**
Displays all orders (initially empty).

**Q5 — Menu Summary**
Shows total items, available/unavailable count, and categories.

---

## 🔹 Day 2–3 — Validation & Order Logic

**Q6 — Validation (Pydantic)**
Validates input fields like quantity, ensuring it is greater than 0.

**Q7 — Helper Functions**
Uses reusable functions like finding menu item and calculating bill.

**Q8 — Create Order**
Creates a new order with proper validation and error handling.

---

## 🔹 Day 4 — CRUD Operations

**Q9 — Delivery Logic**
Adds delivery charge for delivery orders.

**Q10 — Filter Menu**
Filters menu items based on category, price, and availability.

**Q11 — Add Menu Item**
Adds a new food item to the menu.

**Q12 — Update Menu Item**
Updates item price and availability.

**Q13 — Delete Menu Item**
Removes an item from the menu.

---

## 🔹 Day 5 — Cart & Workflow

**Q14 — Cart System**
Allows adding items to cart, updating quantity, and viewing cart.

**Q15 — Checkout System**
Converts cart items into orders and clears the cart.

---

## 🔹 Day 6 — Advanced APIs

**Q16 — Search Menu**
Searches items using keyword (name/category).

**Q17 — Sort Menu**
Sorts items by price, name, or category.

**Q18 — Pagination**
Divides menu items into pages.

**Q19 — Orders Search & Sort**
Searches orders by customer name and sorts by total price.

**Q20 — Combined Browse API**
Combines search, sorting, and pagination in one API.

---

## 🧪 Testing

All APIs were tested using FastAPI Swagger UI:
http://127.0.0.1:8000/docs

---

## 📌 Note

* Screenshots only show outputs
* This file explains the corresponding question logic
