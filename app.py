import csv
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Bikin list kosong buat nampung data dari CSV
    koleksi_produk = []
    
    try:
        # Buka file produk.csv
        # Tambahin encoding='utf-8' biar teks berantakan atau simbol aneh tetep kebaca aman
        with open('produk.csv', mode='r', encoding='utf-8') as file:
            # DictReader ini ajaib, dia otomatis jadiin baris pertama Excel lu sebagai "kunci"
            csv_reader = csv.DictReader(file)
            
            # Masukin setiap baris data ke dalam list koleksi_produk
            for row in csv_reader:
                koleksi_produk.append(row)
                
    except FileNotFoundError:
        print("Waduh, file produk.csv nggak ketemu nih cuy! Pastiin namanya bener.")

    # Kirim datanya ke file index.html persis kayak sebelumnya
    return render_template('index.html', products=koleksi_produk)

if __name__ == '__main__':
    app.run(debug=True)