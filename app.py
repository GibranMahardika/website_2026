from flask import Flask, render_template, request, redirect, url_for
import csv
import datetime

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

@app.route('/pesan/<nama_produk>')
def proses_pesanan(nama_produk):
    # 1. Kumpulin data "Intel" dari user yang ngeklik
    waktu_klik = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_user = request.remote_addr # Ambil IP Address pembeli
    device_user = request.user_agent.string # Ambil info (Pake Chrome, Safari, Android, atau iPhone)

    # 2. Catat datanya ke dalam file log_klik.csv (Otomatis dibikin kalau belum ada)
    with open('log_klik.csv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Tulis baris baru di excel tracker lu
        writer.writerow([waktu_klik, nama_produk, ip_user, device_user])

    # 3. Cari link WhatsApp asli dari barang yang diklik
    link_wa = "https://wa.me/628123456789" # Link cadangan kalau error
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['nama'] == nama_produk:
                    link_wa = row['link_beli']
                    break
    except Exception as e:
        pass

    # 4. Lempar (Redirect) pembeli ke WhatsApp secara otomatis!
    return redirect(link_wa)

if __name__ == '__main__':
    app.run(debug=True)