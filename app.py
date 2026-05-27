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
    # ==========================================
    # 1. KODINGAN PRODUK JAGOAN LU (Biarkan seperti semula)
    # ==========================================
    recommended_products = []
    try:
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                recommended_products.append(row)
    except FileNotFoundError:
        pass

    recommended_products = recommended_products[:6]

    # ==========================================
    # 2. TAMBAHAN BARU: BACA REVIEWS BUAT TESTIMONI
    # ==========================================
    testimonials = []
    try:
        with open('review.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                testimonials.append(row)
    except FileNotFoundError:
        pass

    # Balik urutannya biar review paling bawah (terbaru) muncul duluan,
    # terus potong cuma ambil 3 aja biar desain grid-nya rapi
    testimonials = testimonials[::-1][:3]

    # ==========================================
    # 3. LEMPAR DATA KE HTML
    # ==========================================
    # Jangan lupa tambahin variabel testimonials=testimonials di render_template
    return render_template('index.html', 
                           products=recommended_products, 
                           testimonials=testimonials)

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
    # 1.5 LOGIKA BARU: NGUMPULIN BANYAK GAMBAR
    # ==========================================
    product_images = [product['gambar']] # Gambar utama (pasti ada)
    
    # Cek apakah ada gambar2 dan isinya gak kosong
    if product.get('gambar2') and product['gambar2'].strip() != '':
        product_images.append(product['gambar2'].strip())
        
    # Cek apakah ada gambar3 dan isinya gak kosong
    if product.get('gambar3') and product['gambar3'].strip() != '':
        product_images.append(product['gambar3'].strip())

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
                           avg_rating=avg_rating,
                           product_images=product_images) # <-- INI YANG LUPA LU TARUH TADI CUY

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
    link_wa = "https://wa.me/6289526402565" # Link cadangan kalau error
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