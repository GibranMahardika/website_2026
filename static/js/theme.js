// Fungsi untuk mengatur tema saat halaman dimuat
function applyTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;
  const currentTheme = localStorage.getItem('tema');

  if (currentTheme === 'dark') {
    body.classList.add('dark-mode');
    if (themeToggle) themeToggle.textContent = '☀️ Light Mode';
  } else {
    body.classList.remove('dark-mode');
    if (themeToggle) themeToggle.textContent = '🌙 Dark Mode';
  }
}

// Jalankan pengecekan tema segera setelah script dimuat
applyTheme();

// Logika klik tombol toggle
document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      body.classList.toggle('dark-mode');

      if (body.classList.contains('dark-mode')) {
        localStorage.setItem('tema', 'dark');
        themeToggle.textContent = '☀️ Light Mode';
      } else {
        localStorage.setItem('tema', 'light');
        themeToggle.textContent = '🌙 Dark Mode';
      }
    });
  }
});

/**
 * Fungsi untuk melacak saat produk dilihat oleh pengunjung.
 * @param {string} itemId - Kode unik produk (SKU).
 * @param {string} itemName - Nama produk jamu.
 * @param {string} itemCategory - Kategori produk (contoh: "Jamu Pelangsing", "Jamu Anak").
 * @param {number} itemPrice - Harga produk dalam angka.
 */
function trackProductView(itemId, itemName, itemCategory, itemPrice) {
  // Memeriksa apakah script tracking (gtag) sudah dimuat di website
  if (typeof gtag !== 'undefined') {
    gtag('event', 'view_item', {
      currency: 'IDR',
      value: itemPrice,
      items: [
        {
          item_id: itemId,
          item_name: itemName,
          item_category: itemCategory, // Di sinilah kategori jamu Anda dimasukkan!
          price: itemPrice,
          quantity: 1,
        },
      ],
    });
    console.log(
      'Tracking berhasil dikirim untuk: ' +
        itemName +
        ' | Kategori: ' +
        itemCategory,
    );
  } else {
    console.warn('Sistem tracking belum siap di halaman ini.');
  }
}

// ==========================================
// CARA MENGGUNAKAN KODE DI ATAS (Contoh)
// ==========================================

// Contoh 1: Dipanggil saat halaman produk "Jamu Pelangsing" dimuat
// trackProductView("JP-001", "Jamu Ramping Ayu", "Jamu Pelangsing", 50000);

// Contoh 2: Dipanggil saat halaman produk "Jamu Anak" dimuat
// trackProductView("JA-002", "Jamu Tumbuh Cerdas Anak", "Jamu Anak", 35000);
