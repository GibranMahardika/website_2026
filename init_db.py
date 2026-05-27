import sqlite3

conn = sqlite3.connect("grizelline.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    deskripsi TEXT,
    harga INTEGER DEFAULT 0,
    gambar TEXT,
    gambar2 TEXT,
    gambar3 TEXT,
    link_beli TEXT,
    kategori TEXT,
    detail_produk TEXT,
    is_recommended INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    nama_produk TEXT,
    nama_pembeli TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    ulasan TEXT,
    tanggal TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS click_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    nama_produk TEXT,
    waktu_klik TEXT,
    ip_user TEXT,
    device_user TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

conn.commit()
conn.close()

print("Database grizelline.db berhasil dibuat.")