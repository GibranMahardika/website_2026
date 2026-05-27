import csv
import re
import sqlite3

def make_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def clean_price(price_text):
    if not price_text:
        return 0

    angka = re.sub(r'[^0-9]', '', price_text)
    return int(angka) if angka else 0

conn = sqlite3.connect("grizelline.db")
cursor = conn.cursor()

with open("produk.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        nama = row.get("nama", "").strip()

        if not nama:
            continue

        slug = make_slug(nama)
        harga = clean_price(row.get("harga", ""))

        cursor.execute("""
            INSERT OR IGNORE INTO products
            (nama, slug, deskripsi, harga, gambar, gambar2, gambar3, link_beli, kategori, detail_produk, is_recommended)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nama,
            slug,
            row.get("deskripsi", "").strip(),
            harga,
            row.get("gambar", "").strip(),
            row.get("gambar2", "").strip(),
            row.get("gambar3", "").strip(),
            row.get("link_beli", "").strip(),
            row.get("kategori", "").strip(),
            row.get("detail_produk", "").strip(),
            1
        ))

conn.commit()
conn.close()

print("Data produk berhasil masuk ke database.")