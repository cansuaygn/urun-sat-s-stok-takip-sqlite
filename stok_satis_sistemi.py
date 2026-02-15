import sqlite3
from datetime import datetime

DB_NAME = "stok_satis.db"


def connect_db():
    # Veritabanına bağlanmak için her seferinde bunu kullanıyorum
    return sqlite3.connect(DB_NAME)


def create_tables():
    # Program ilk açıldığında tablolar yoksa otomatik oluşsun diye yazdım
    conn = connect_db()
    cursor = conn.cursor()

    sql_products = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """

    sql_sales = """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """

    cursor.execute(sql_products)
    cursor.execute(sql_sales)

    conn.commit()
    conn.close()


def add_product(name, price, stock):
    # Yeni ürün eklemek için INSERT kullandım
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO products (name, price, stock)
    VALUES (?, ?, ?)
    """

    cursor.execute(sql, (name, price, stock))

    conn.commit()
    conn.close()


def list_products():
    # Ürünleri ekranda görmek için basit bir SELECT yaptım
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT id, name, price, stock FROM products"
    cursor.execute(sql)

    products = cursor.fetchall()
    conn.close()

    print("\n--- ÜRÜNLER ---")
    if len(products) == 0:
        print("Hiç ürün yok.")
        return

    for p in products:
        print(f"ID: {p[0]} | {p[1]} | {p[2]} TL | Stok: {p[3]}")


def get_product_by_id(product_id):
    # Satış yaparken veya silerken ürün var mı diye kontrol etmek için yazdım
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT id, name, price, stock FROM products WHERE id = ?"
    cursor.execute(sql, (product_id,))

    product = cursor.fetchone()
    conn.close()

    return product


def decrease_stock(product_id, quantity):
    # Satıştan sonra stok düşsün diye UPDATE kullandım
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    UPDATE products
    SET stock = stock - ?
    WHERE id = ?
    """

    cursor.execute(sql, (quantity, product_id))

    conn.commit()
    conn.close()


def add_sale(product_id, quantity, total_price):
    # Satış yapınca sales tablosuna kayıt düşmesi için bunu yazdım
    conn = connect_db()
    cursor = conn.cursor()

    sale_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    sql = """
    INSERT INTO sales (product_id, quantity, total_price, sale_date)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(sql, (product_id, quantity, total_price, sale_date))

    conn.commit()
    conn.close()


def make_sale(product_id, quantity):
    # Satış yapmadan önce ürün var mı ve stok yeterli mi kontrol ediyorum
    product = get_product_by_id(product_id)

    if product is None:
        print("Bu ID ile ürün bulunamadı.")
        return

    pid, name, price, stock = product

    if quantity <= 0:
        print("Adet 0 veya negatif olamaz.")
        return

    if quantity > stock:
        print(f"Stok yetersiz! Mevcut stok: {stock}")
        return

    total_price = price * quantity

    # Satış kaydını ekliyorum
    add_sale(product_id, quantity, total_price)

    # Sonra stok düşürüyorum
    decrease_stock(product_id, quantity)

    print(f"Satış tamamlandı: {name} x{quantity} | Toplam: {total_price} TL")


def list_sales():
    # Satışları ürün ismiyle beraber görmek için JOIN kullandım
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    SELECT sales.id, products.name, sales.quantity, sales.total_price, sales.sale_date
    FROM sales
    JOIN products ON sales.product_id = products.id
    ORDER BY sales.id DESC
    """

    cursor.execute(sql)
    sales = cursor.fetchall()
    conn.close()

    print("\n--- SATIŞLAR ---")
    if len(sales) == 0:
        print("Hiç satış yok.")
        return

    for s in sales:
        print(f"SatışID: {s[0]} | Ürün: {s[1]} | Adet: {s[2]} | Toplam: {s[3]} TL | Tarih: {s[4]}")


def total_revenue():
    # Toplam ciroyu hesaplamak için SUM kullandım
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT SUM(total_price) FROM sales"
    cursor.execute(sql)

    result = cursor.fetchone()[0]
    conn.close()

    if result is None:
        result = 0

    print(f"\nToplam ciro: {result} TL")


def delete_product(product_id):
    # Ürün silme kısmını ID üzerinden yaptım
    product = get_product_by_id(product_id)

    if product is None:
        print("Bu ID ile ürün bulunamadı.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    sql = "DELETE FROM products WHERE id = ?"
    cursor.execute(sql, (product_id,))

    conn.commit()
    conn.close()

    print("Ürün silindi.")


def update_product(product_id, new_price, new_stock):
    # Ürün fiyatını ve stok miktarını güncellemek için yazdım
    product = get_product_by_id(product_id)

    if product is None:
        print("Bu ID ile ürün bulunamadı.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    UPDATE products
    SET price = ?, stock = ?
    WHERE id = ?
    """

    cursor.execute(sql, (new_price, new_stock, product_id))

    conn.commit()
    conn.close()

    print("Ürün güncellendi.")


def best_selling_product():
    # En çok satılan ürünü bulmak için GROUP BY + SUM kullandım
    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    SELECT products.name, SUM(sales.quantity) as toplam_satis
    FROM sales
    JOIN products ON sales.product_id = products.id
    GROUP BY products.name
    ORDER BY toplam_satis DESC
    LIMIT 1
    """

    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Henüz satış yapılmamış.")
        return

    print(f"\nEn çok satılan ürün: {result[0]} | Toplam satış: {result[1]} adet")


def menu():
    print("\n--- STOK & SATIŞ SİSTEMİ ---")
    print("1 - Ürün ekle")
    print("2 - Ürünleri listele")
    print("3 - Satış yap")
    print("4 - Satışları listele")
    print("5 - Toplam ciro")
    print("6 - Ürün sil (ID ile)")
    print("7 - Ürün güncelle (fiyat/stok)")
    print("8 - En çok satılan ürün")
    print("9 - Çıkış")


def main():
    create_tables()

    while True:
        menu()
        secim = input("Seçim: ").strip()

        if secim == "1":
            name = input("Ürün adı: ").strip()
            price = float(input("Fiyat: "))
            stock = int(input("Stok: "))

            add_product(name, price, stock)
            print("Ürün eklendi.")

        elif secim == "2":
            list_products()

        elif secim == "3":
            list_products()
            product_id = int(input("Satılacak ürün ID: "))
            quantity = int(input("Kaç adet satıldı: "))

            make_sale(product_id, quantity)

        elif secim == "4":
            list_sales()

        elif secim == "5":
            total_revenue()

        elif secim == "6":
            list_products()
            product_id = int(input("Silinecek ürün ID: "))
            delete_product(product_id)

        elif secim == "7":
            list_products()
            product_id = int(input("Güncellenecek ürün ID: "))
            new_price = float(input("Yeni fiyat: "))
            new_stock = int(input("Yeni stok: "))
            update_product(product_id, new_price, new_stock)

        elif secim == "8":
            best_selling_product()

        elif secim == "9":
            print("Çıkış yapıldı.")
            break

        else:
            print("Hatalı seçim.")


main()
