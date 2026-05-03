from flask import Flask, render_template, request, redirect, url_for
import csv
import datetime

app = Flask(__name__)

# === JURUS SAKTI: Bikin daftar kategori tersedia di SEMUA halaman HTML ===
@app.context_processor
def inject_kategori():
    kategori_unik = set() # Pakai 'set' biar nama kategori yang sama nggak dobel
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                # Ambil nama kategori kalau ada isinya
                if 'kategori' in row and row['kategori'].strip():
                    kategori_unik.add(row['kategori'].strip())
    except FileNotFoundError:
        pass
    
    # Kembalikan datanya dalam bentuk list yang udah diurutin sesuai abjad
    return dict(daftar_kategori=sorted(list(kategori_unik)))

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
    # Bikin list kosong buat nampung produk jagoan
    recommended_products = []
    
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                recommended_products.append(row)
    except FileNotFoundError:
        pass

    # Trik MVP: Ambil maksimal 6 produk teratas aja dari CSV buat nangkring di halaman depan
    recommended_products = recommended_products[:6]

    # Kirim datanya ke index.html dengan nama 'products'
    return render_template('index.html', products=recommended_products)
# ROUTE BARU: Halaman Detail Produk
# Tambahin ini di app.py lu ya!
@app.route('/produk/<nama_produk>')
def detail_produk(nama_produk):
    # ==========================================
    # 1. LOGIKA LAMA LU (Nyari info jamu)
    # ==========================================
    product = None
    with open('produk.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['nama'] == nama_produk:
                product = row
                break
                
    # Kalau produk gak ketemu, lempar ke home
    if not product:
        return redirect(url_for('home'))

    # ==========================================
    # 2. LOGIKA BARU (Nyari review jamunya)
    # ==========================================
    reviews_list = []
    total_bintang = 0
    
    try:
        with open('reviews.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['nama_produk'] == nama_produk:
                    reviews_list.append(row)
                    total_bintang += int(row['rating'])
    except FileNotFoundError:
        pass 
        
    review_count = len(reviews_list)
    
    if review_count > 0:
        avg_rating = round(total_bintang / review_count, 1)
    else:
        avg_rating = 0.0

    # ==========================================
    # 3. LEMPAR SEMUA DATANYA KE HTML
    # ==========================================
    return render_template('product_detail.html', 
                           product=product, 
                           reviews=reviews_list, 
                           review_count=review_count, 
                           avg_rating=avg_rating)

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