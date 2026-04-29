import csv
from flask import Flask, render_template, abort

app = Flask(__name__)

# Fungsi bantuan untuk baca CSV biar kodenya rapi
def get_products():
    products = []
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                products.append(row)
    except FileNotFoundError:
        pass
    return products

@app.route('/')
def home():
    # Kita bikin dictionary (kamus) buat ngelompokin barang
    products_by_category = {}
    
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ambil nama kategori dari CSV, kalau kosong kita masukin ke 'Lainnya'
                kat = row.get('kategori', 'Lainnya')
                
                # Kalau kategorinya belum ada di list, bikin baru
                if kat not in products_by_category:
                    products_by_category[kat] = []
                    
                # Masukin barangnya ke kategori yang sesuai
                products_by_category[kat].append(row)
                
    except FileNotFoundError:
        pass

    # Perhatiin: yang dikirim sekarang namanya products_by_category
    return render_template('index.html', products_by_category=products_by_category)

# ROUTE BARU: Halaman Detail Produk
# Tambahin ini di app.py lu ya!
@app.route('/produk/<nama_produk>')
def detail_produk(nama_produk):
    # Mengambil data dari CSV
    products = []
    with open('produk.csv', mode='r', encoding='utf-8') as file:
        import csv
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
            
    # Nyari barang yang namanya pas diklik
    item = next((p for p in products if p['nama'] == nama_produk), None)
    
    if item is None:
        return "Barang tidak ditemukan", 404
        
    return render_template('product_detail.html', product=item)

# ROUTE BARU: Halaman Kategori Spesifik
@app.route('/kategori/<nama_kategori>')
def kategori_produk(nama_kategori):
    products_in_category = []
    
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                # Cek apakah barang ini masuk ke kategori yang diklik user
                if row.get('kategori', '') == nama_kategori:
                    products_in_category.append(row)
    except FileNotFoundError:
        pass
        
    return render_template('kategori.html', 
                           products=products_in_category, 
                           kategori=nama_kategori)

if __name__ == '__main__':
    app.run(debug=True)