import sqlite3
def is_low_stock(quantity, threshold=10):
    return quantity < threshold

def calculate_total(price, quantity):
    return price * quantity

def validate_product(name, price, quantity):
    return name != "" and price >= 0 and quantity >= 0

# Unit tests
def test_low_stock_true():
    assert is_low_stock(5) is True

def test_calculate_total():
    assert calculate_total(20, 3) == 60

def test_validate_product():
    assert validate_product("Mouse", 20, 5) is True

# Integration test 1: product insertion
def test_add_product_to_database():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE product (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Supplier TEXT,
            name TEXT,
            price REAL,
            qty INTEGER,
            status TEXT
        )
    """)

    cur.execute(
        "INSERT INTO product(Category, Supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
        ("Electronics", "ABC Supplier", "Mouse", 20, 5, "Active")
    )

    con.commit()
    cur.execute("SELECT name, qty FROM product WHERE name='Mouse'")
    result = cur.fetchone()

    assert result == ("Mouse", 5)
    con.close()


# Integration test 2: low stock query
def test_low_stock_products_from_database():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE product (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Supplier TEXT,
            name TEXT,
            price REAL,
            qty INTEGER,
            status TEXT
        )
    """)

    cur.execute(
        "INSERT INTO product(Category, Supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
        ("Electronics", "ABC Supplier", "Keyboard", 30, 4, "Active")
    )

    cur.execute("SELECT name FROM product WHERE qty < 10")
    result = cur.fetchone()

    assert result == ("Keyboard",)
    con.close()

# Regression test
def test_existing_total_calculation_still_works():
    assert calculate_total(15, 4) == 60