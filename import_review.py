import csv
import sqlite3

conn = sqlite3.connect("grizelline.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

with open("review.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        nama_produk = row.get("nama_produk", "").strip()

        product = cursor.execute("""
            SELECT id FROM products
            WHERE nama = ?
        """, (nama_produk,)).fetchone()

        product_id = product["id"] if product else None

        try:
            rating = int(row.get("rating", 5))
        except:
            rating = 5

        cursor.execute("""
            INSERT INTO reviews
            (product_id, nama_produk, nama_pembeli, rating, ulasan, tanggal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product_id,
            nama_produk,
            row.get("nama_pembeli", "").strip(),
            rating,
            row.get("ulasan", "").strip(),
            row.get("tanggal", "").strip()
        ))

conn.commit()
conn.close()

print("Data review berhasil masuk ke database.")