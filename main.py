"""
Restaurant POS System
Author: Muhammad Amjad Aziz Shah
Description: A desktop Point-of-Sale application built with Python (Tkinter + SQLite)
             supporting admin menu management and customer order processing.
"""

import tkinter as tk
import sqlite3


# ============================================================
# DATABASE SETUP
# ============================================================

def get_connection():
    """Return a new SQLite database connection."""
    return sqlite3.connect("restaurant.db")


def init_db():
    """Initialize database tables and default settings."""
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            category TEXT,
            item     TEXT,
            price    INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key   TEXT PRIMARY KEY,
            value REAL
        )
    """)

    # Default tax rate: 5%
    cur.execute("INSERT OR IGNORE INTO settings VALUES ('tax', 5)")
    con.commit()
    con.close()


# ============================================================
# DATA LAYER
# ============================================================

menu = {}       # { category: { item: price } }
order = {}      # { item: (quantity, price) }
food_tax = 5    # Tax percentage (loaded from DB)


def load_data():
    """Load menu items and tax rate from the database into memory."""
    global food_tax
    menu.clear()

    con = get_connection()
    cur = con.cursor()

    for category, item, price in cur.execute("SELECT * FROM menu"):
        menu.setdefault(category, {})[item] = price

    cur.execute("SELECT value FROM settings WHERE key = 'tax'")
    result = cur.fetchone()
    if result:
        food_tax = result[0]

    con.close()


# ============================================================
# VALIDATION HELPERS
# ============================================================

def valid_text(value):
    """Return True if value is non-empty, non-numeric text."""
    return bool(value) and not value.isdigit() and not value[0].isdigit()


def valid_int(value):
    """Return True if value is a positive integer string."""
    return value.isdigit() and int(value) > 0


# ============================================================
# UI NAVIGATION
# ============================================================

def show_frame(frame):
    """Hide all frames and show the given frame."""
    for f in (main_frame, admin_frame, customer_frame):
        f.pack_forget()
    frame.pack(fill="both", expand=True)
    status.set("")


def clear_form():
    """Remove all widgets from the admin form panel."""
    for widget in form_frame.winfo_children():
        widget.destroy()


# ============================================================
# ADMIN — AUTHENTICATION
# ============================================================

def admin_login():
    """Validate admin password and navigate to admin panel."""
    if admin_pass.get() != "admin123":
        status.set("❌ Wrong admin password")
        return
    show_frame(admin_frame)


# ============================================================
# ADMIN — CATEGORY MANAGEMENT
# ============================================================

def form_add_category():
    clear_form()
    form_title("Add Category")
    form_field("Category Name", cat_var)
    form_submit(add_category)


def add_category():
    c = cat_var.get().strip()
    if not valid_text(c):
        status.set("❌ Invalid category name")
        return
    if c in menu:
        status.set("❌ Category already exists")
        return
    menu[c] = {}
    status.set(f"✅ Category '{c}' added")
    refresh_menu_list()


def form_delete_category():
    clear_form()
    form_title("Delete Category")
    form_field("Category Name", cat_var)
    form_submit(delete_category)


def delete_category():
    c = cat_var.get().strip()
    if c not in menu:
        status.set("❌ Category not found")
        return
    del menu[c]
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM menu WHERE category = ?", (c,))
    con.commit()
    con.close()
    refresh_menu_list()
    status.set(f"✅ Category '{c}' deleted")


# ============================================================
# ADMIN — ITEM MANAGEMENT
# ============================================================

def form_add_item():
    clear_form()
    form_title("Add Item")
    form_field("Category", cat_var)
    form_field("Item Name", item_var)
    form_field("Price (Rs)", price_var)
    form_submit(add_item)


def add_item():
    c, i, p = cat_var.get().strip(), item_var.get().strip(), price_var.get().strip()
    if c not in menu:
        status.set("❌ Category not found")
        return
    if not valid_text(i):
        status.set("❌ Invalid item name")
        return
    if not valid_int(p):
        status.set("❌ Price must be a positive number")
        return
    menu[c][i] = int(p)
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO menu VALUES (?, ?, ?)", (c, i, p))
    con.commit()
    con.close()
    refresh_menu_list()
    status.set(f"✅ '{i}' added to {c}")


def form_update_item():
    clear_form()
    form_title("Update Item Price")
    form_field("Category", cat_var)
    form_field("Item Name", item_var)
    form_field("New Price (Rs)", price_var)
    form_submit(update_item)


def update_item():
    c, i, p = cat_var.get().strip(), item_var.get().strip(), price_var.get().strip()
    if c not in menu or i not in menu.get(c, {}):
        status.set("❌ Item not found")
        return
    if not valid_int(p):
        status.set("❌ Invalid price")
        return
    menu[c][i] = int(p)
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE menu SET price = ? WHERE category = ? AND item = ?", (p, c, i))
    con.commit()
    con.close()
    refresh_menu_list()
    status.set(f"✅ '{i}' price updated to Rs {p}")


def form_delete_item():
    clear_form()
    form_title("Delete Item")
    form_field("Category", cat_var)
    form_field("Item Name", item_var)
    form_submit(delete_item)


def delete_item():
    c, i = cat_var.get().strip(), item_var.get().strip()
    if c not in menu or i not in menu.get(c, {}):
        status.set("❌ Item not found")
        return
    del menu[c][i]
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM menu WHERE category = ? AND item = ?", (c, i))
    con.commit()
    con.close()
    refresh_menu_list()
    status.set(f"✅ '{i}' deleted")


# ============================================================
# ADMIN — TAX SETTINGS
# ============================================================

def form_set_tax():
    clear_form()
    form_title("Set Tax Rate (%)")
    form_field("Tax (%)", tax_var)
    form_submit(set_tax)


def set_tax():
    global food_tax
    t = tax_var.get().strip()
    if not valid_int(t):
        status.set("❌ Tax must be a positive number")
        return
    food_tax = int(t)
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE settings SET value = ? WHERE key = 'tax'", (t,))
    con.commit()
    con.close()
    status.set(f"✅ Tax updated to {t}%")


# ============================================================
# CUSTOMER — ORDER MANAGEMENT
# ============================================================

def refresh_menu_list():
    """Reload the menu listbox from the in-memory menu dictionary."""
    menu_list.delete(0, tk.END)
    for category, items in menu.items():
        menu_list.insert(tk.END, f"── {category} ──")
        for item, price in items.items():
            menu_list.insert(tk.END, f"  {item} - Rs {price}")


def add_to_order():
    """Add the selected menu item with given quantity to the order."""
    selected = menu_list.get(tk.ACTIVE)
    quantity = qty_var.get().strip()

    if "Rs" not in selected:
        status.set("❌ Please select a menu item (not a category header)")
        return
    if not valid_int(quantity):
        status.set("❌ Enter a valid quantity")
        return

    # Parse "  Item Name - Rs 250" → item="Item Name", price=250
    parts = selected.strip().split(" - Rs ")
    item_name = parts[0].strip()
    price = int(parts[1])

    order[item_name] = (int(quantity), price)
    refresh_order_list()
    status.set(f"✅ {item_name} x{quantity} added to order")


def refresh_order_list():
    """Reload the order listbox from the in-memory order dictionary."""
    order_list.delete(0, tk.END)
    for item, (qty, price) in order.items():
        order_list.insert(tk.END, f"{item}  x{qty}  = Rs {qty * price}")


def remove_from_order():
    """Remove the selected item from the current order."""
    selection = order_list.curselection()
    if not selection:
        status.set("❌ Select an item to remove")
        return
    item_name = order_list.get(selection[0]).split("  x")[0]
    del order[item_name]
    refresh_order_list()
    status.set(f"✅ '{item_name}' removed from order")


def show_final_bill():
    """Calculate subtotal, tax, and total, then display the bill."""
    if not order:
        status.set("❌ No items in order")
        return
    subtotal = sum(qty * price for qty, price in order.values())
    tax_amount = subtotal * food_tax / 100
    total = subtotal + tax_amount
    status.set(
        f"  Subtotal: Rs {subtotal:.2f}  |  "
        f"Tax ({food_tax}%): Rs {tax_amount:.2f}  |  "
        f"💰 Total: Rs {total:.2f}"
    )


# ============================================================
# UI HELPER WIDGETS
# ============================================================

def form_title(text):
    tk.Label(form_frame, text=text, font=("Arial", 14, "bold")).pack(pady=10)


def form_field(label, variable):
    tk.Label(form_frame, text=label).pack()
    tk.Entry(form_frame, textvariable=variable, width=25).pack(pady=2)


def form_submit(command):
    tk.Button(form_frame, text="Submit", width=15, command=command).pack(pady=10)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

init_db()
load_data()

root = tk.Tk()
root.title("Restaurant POS System")
root.geometry("960x560")
root.resizable(False, False)

# Shared variables
status   = tk.StringVar()
cat_var  = tk.StringVar()
item_var = tk.StringVar()
price_var = tk.StringVar()
tax_var  = tk.StringVar()
qty_var  = tk.StringVar()

# ── Main / Login Frame ──────────────────────────────────────
main_frame = tk.Frame(root)

tk.Label(main_frame, text="🍽  Restaurant POS System",
         font=("Arial", 22, "bold")).pack(pady=30)

tk.Label(main_frame, text="Admin Password", font=("Arial", 10)).pack()
admin_pass = tk.Entry(main_frame, show="*", width=20)
admin_pass.pack(pady=4)

tk.Button(main_frame, text="Admin Login",    width=18, command=admin_login).pack(pady=4)
tk.Button(main_frame, text="Customer Menu",  width=18,
          command=lambda: [refresh_menu_list(), show_frame(customer_frame)]).pack(pady=4)

tk.Label(main_frame, textvariable=status, fg="red").pack(pady=10)
main_frame.pack()

# ── Admin Frame ─────────────────────────────────────────────
admin_frame = tk.Frame(root)
tk.Label(admin_frame, text="Admin Panel", font=("Arial", 18, "bold")).pack(pady=8)

btn_panel = tk.Frame(admin_frame)
btn_panel.pack(side=tk.LEFT, padx=15, pady=10)

admin_buttons = [
    ("Add Category",    form_add_category),
    ("Delete Category", form_delete_category),
    ("Add Item",        form_add_item),
    ("Update Item",     form_update_item),
    ("Delete Item",     form_delete_item),
    ("Set Tax",         form_set_tax),
    ("← Back",          lambda: show_frame(main_frame)),
]
for label, command in admin_buttons:
    tk.Button(btn_panel, text=label, width=20, command=command).pack(pady=3)

form_frame = tk.Frame(admin_frame, relief=tk.GROOVE, bd=1, padx=20, pady=10)
form_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)

# ── Customer Frame ───────────────────────────────────────────
customer_frame = tk.Frame(root)

tk.Label(customer_frame, text="Customer Order",
         font=("Arial", 14, "bold")).pack(pady=6)

list_row = tk.Frame(customer_frame)
list_row.pack()

tk.Label(list_row, text="Menu", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=20)
tk.Label(list_row, text="Your Order", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=20)

menu_list = tk.Listbox(list_row, width=42, height=18, font=("Arial", 10))
menu_list.grid(row=1, column=0, padx=10)

order_list = tk.Listbox(list_row, width=36, height=18, font=("Arial", 10))
order_list.grid(row=1, column=1, padx=10)

ctrl = tk.Frame(list_row)
ctrl.grid(row=1, column=2, padx=10)

tk.Label(ctrl, text="Quantity").pack(pady=4)
tk.Entry(ctrl, textvariable=qty_var, width=8).pack()
tk.Button(ctrl, text="Add to Order",   width=14, command=add_to_order).pack(pady=6)
tk.Button(ctrl, text="Remove Item",    width=14, command=remove_from_order).pack(pady=2)
tk.Button(ctrl, text="Final Bill",     width=14, command=show_final_bill).pack(pady=6)
tk.Button(ctrl, text="← Back",         width=14, command=lambda: show_frame(main_frame)).pack(pady=2)

# ── Status Bar ───────────────────────────────────────────────
tk.Label(root, textvariable=status, fg="blue",
         font=("Arial", 10), anchor="w").pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=4)

root.mainloop()
