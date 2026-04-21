# 🍽️ Restaurant POS System

A desktop **Point-of-Sale (POS)** application built with **Python**, using **Tkinter** for the GUI and **SQLite** for persistent data storage. Developed as a university project for Iqra University Islamabad.

---

## 📸 Features

### 👨‍💼 Admin Panel
- Secure password-protected login
- Add / Delete menu categories
- Add / Update / Delete menu items with prices
- Configure tax rate (saved to database)

### 🛒 Customer Panel
- Browse full menu organized by category
- Add items to order with custom quantity
- Remove items from order
- Generate final bill with tax breakdown

---

## 🛠️ Tech Stack

| Layer       | Technology        |
|-------------|-------------------|
| Language    | Python 3.x        |
| GUI         | Tkinter (built-in)|
| Database    | SQLite3 (built-in)|

> No external libraries required — runs on any system with Python 3 installed.

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/restaurant-pos.git
cd restaurant-pos
```

**2. Run the application**
```bash
python main.py
```

> Make sure Python 3 is installed. No pip installs needed.

---

## 🔐 Default Credentials

| Role  | Password   |
|-------|------------|
| Admin | `admin123` |

---

## 📁 Project Structure

```
restaurant-pos/
│
├── main.py          # Main application (UI + logic)
├── restaurant.db    # SQLite database (auto-created on first run)
└── README.md        # Project documentation
```

---

## 📊 Database Schema

**Table: `menu`**
| Column   | Type    | Description        |
|----------|---------|--------------------|
| category | TEXT    | Menu category name |
| item     | TEXT    | Item name          |
| price    | INTEGER | Item price (Rs)    |

**Table: `settings`**
| Column | Type | Description          |
|--------|------|----------------------|
| key    | TEXT | Setting name         |
| value  | REAL | Setting value        |

---

## 💡 Concepts Demonstrated

- Object-oriented design patterns in Python
- GUI development with Tkinter
- SQLite database integration (CRUD operations)
- Input validation and error handling
- Separation of data, logic, and UI layers

---

## 👨‍💻 Author

**Muhammad Amjad Aziz Shah**  
BS Software Engineering — Iqra University, Islamabad (Semester 6)  
📧 amjadaziz@email.com  
🔗 [GitHub Profile](https://github.com/YOUR_USERNAME)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
