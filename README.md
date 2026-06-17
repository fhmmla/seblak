# 🍜 SEBLAK Frontend (GUI Aplikasi Manajemen Data Mahasiswa)

**Nama:** Fahmi Maulana Fadila  
**NIM:** 241011450401  
**Kelas:** 03TPLE005  
**Mata Kuliah:** Algoritma Dan Pemrograman II  
**Jenis Ujian:** UAS  

---

## 📖 Tentang Project

Ini adalah repositori **Frontend Web (GUI)** untuk proyek **SEBLAK (Sistem Evaluasi Belajar Lab Akademik & Kelas)**. Bertindak sebagai antarmuka (UI) dari backend REST API, aplikasi ini dirancang khusus untuk memenuhi kriteria tugas pembuatan aplikasi "GUI Sederhana" yang modern dan dinamis. 

Sistem ini dibangun menggunakan arsitektur perpaduan antara **Flask (Python)** sebagai web server sekaligus *API Proxy* dan **Vanilla JavaScript** (ES6) + **TailwindCSS** di sisi klien (browser) untuk menyajikan pengalaman pengguna yang sangat interaktif, responsif, dan estetis.

> **Catatan:** Project ini berfokus pada sisi **Frontend (GUI Client)**.

🔗 **Repository:** [https://github.com/fhmmla/seblak](https://github.com/fhmmla/seblak)  
🌍 **Live Demo Frontend:** [https://seblak-pedas.vercel.app/](https://seblak-pedas.vercel.app/)  
⚙️ **Live API Backend:** [https://seblak-api.onrender.com/](https://seblak-api.onrender.com/)  
⚖️ **Lisensi:** MIT License

---

## 🏗️ Struktur Project

```
Sourcecode/
├── static/
│   └── js/
│       └── api.js          # Sentralisasi logika pemanggilan API (Fetch), Token JWT, dan Toast UI
├── templates/
│   ├── base.html           # Layout dasar Jinja2 (Navbar, Sidebar, Skeleton dasar)
│   ├── login.html          # Halaman autentikasi JWT
│   ├── dashboard.html      # Halaman utama (CRUD Mahasiswa, Searching, Sorting, Timer Eksekusi)
│   ├── form_mahasiswa.html # Halaman tambah/edit data mahasiswa (Validasi Form)
│   ├── penilaian.html      # Halaman inovasi penilaian praktikum (Timer Sesi, Gamifikasi Top 10)
│   └── settings.html       # Halaman pengaturan sistem (Fitur Export Backup File I/O)
├── app.py                  # Entry point Flask (Web Server & Proxy API routing)
├── requirements.txt        # Daftar dependensi library (Flask, requests)
└── venv/                   # Virtual environment Python
```

---

## 🔧 Cara Menjalankan

### 1. Setup Virtual Environment
```bash
cd Sourcecode
python -m venv venv
```

### 2. Aktifkan Virtual Environment
```bash
# Windows (PowerShell)
.\venv\Scripts\Activate

# Windows (Git Bash)
source venv/Scripts/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi
Pastikan backend (FastAPI) SEBLAK Anda sudah berjalan terlebih dahulu.
Frontend ini secara default melakukan *proxy* ke `http://127.0.0.1:8000`. Jika URL backend Anda berbeda, silakan ubah variabel `BASE_API_URL` di dalam file `app.py`.

### 5. Jalankan Server
```bash
python app.py
```
Aplikasi GUI sekarang dapat diakses melalui browser Anda di: `http://127.0.0.1:5000`

---

## 📋 Pemenuhan Kriteria Arahan Tugas (UAS)

Berdasarkan instruksi *"Buatlah sebuah aplikasi Manajemen Data Mahasiswa berbasis teks atau GUI sederhana"*, frontend ini mewujudkan kriteria tersebut dalam bentuk visual berbasis web:

### 1. CRUD (Input, Edit, Hapus, Tampilkan)
Beroperasi pada halaman **Dashboard Mahasiswa**, fitur ini mengelola representasi data mahasiswa secara visual:
- **Input & Edit**: Diakomodasi oleh formulir interaktif di `form_mahasiswa.html`.
- **Hapus**: Menggunakan komponen *Popover Modal* untuk mencegah penghapusan tidak disengaja.
- **Implementasi Fungsi, Array, dan Pointer**:
  - **Fungsi**: Logika dipecah menjadi fungsi modular di `api.js` (contoh: `getMahasiswa()`, `deleteMahasiswa()`).
  - **Array**: Response data di-_parsing_ ke dalam struktur data *Array of Objects* di JavaScript.
  - **Pointer**: Manipulasi *DOM (Document Object Model)* dan pengelolaan memori dengan mereferensikan memori variabel objek *array* secara aman.

### 2. Penyimpanan dan Pembacaan Data dari File (File I/O)
Kriteria File I/O diimplementasikan secara interaktif di halaman **Pengaturan**. Melalui sebuah tombol "Export & Backup Database", *frontend* memicu *backend* untuk mengambil data, lalu *browser* menginisiasi pembacaan respon file fisik berformat `.json` yang langsung terunduh ke perangkat *local* pengguna.

### 3. Penerapan Konsep OOP
Sebagian besar logika terdistribusi di *backend*, namun di *frontend* interaksi antarmuka memanfaatkan konsep OOP dasar Javascript. Konsep objek JSON diubah dan dipetakan (*mapping*) ke dalam struktur antarmuka UI komponen secara tertutup (*Encapsulation* state pada variabel-variabel global).

### 4. Fitur Pencarian Data (Linear, Sequential, Binary Search)
Melalui *Dashboard*, UI menyediakan opsi *Chips* dinamis untuk memilih algoritma:
- Pengguna dapat memilih mencari *exact NIM* menggunakan algoritma **Linear** atau **Binary Search**.
- Pengguna dapat memasukkan "Kata Kunci Acak" untuk menggunakan **Sequential Search** yang melintas berbagai field tabel.

### 5. Fitur Pengurutan Data (Insertion & Selection Sort)
Terdapat *Chips Selector* di *Dashboard* di mana pengguna dapat memerintahkan sistem untuk melakukan *Sorting* secara real-time. Pilihan algoritma (**Insertion** atau **Selection Sort**) dapat dikombinasikan dengan kunci atribut seperti (berdasarkan NIM atau berdasar Nama).

### 6. Validasi Input Menggunakan Regular Expression (Regex)
Selain divalidasi oleh Pydantic di *backend*, formulir *Input/Edit* di sisi klien (*frontend*) juga memanfaatkan Regex bawaan HTML5 (`pattern="[0-9]{12}"`) untuk memastikan NIM adalah mutlak 12 digit numerik sebelum *request* dikirim ke server.

### 7. Penanganan Error (Try-Catch & Exception)
Setiap pemanggilan API yang dilakukan oleh fungsi di `api.js` dibungkus kuat dalam algoritma `try...catch`. Kegagalan fatal seperti Server Mati (*Network Error*) dapat ditangkap (*catch*) dan sistem tidak akan mogok, melainkan menampilkan notifikasi visual ramah pengguna berupa **Toast UI** (contoh: "Gagal terhubung ke server. Periksa koneksi internet.").

### 8. Estimasi Time Complexity & Pengukuran UI
Sebagai pembuktian empiris untuk *Time Complexity* operasi *Searching* dan *Sorting*, terdapat fitur **Indikator Waktu Eksekusi (⏱️ ms)**. Setiap kali pengguna menekan tombol cari/urutkan, skrip akan menghitung selisih durasi `performance.now()` yang merender waktu aktual eksekusi dalam ukuran satuan milidetik pada halaman tabel utama.

### 9. Guidelines & Best Practices
- **Modularisasi Kode**: File-file dipecah secara sistematis: `app.py` untuk *Routing Proxy*, `api.js` sentralisasi *fetch*, dan pemisahan layout menggunakan `Jinja2 Templates`.
- **Penamaan Variabel**: Menggunakan standar *camelCase* untuk JavaScript dan *snake_case* untuk Python.

---

## 🌟 Inovasi Tambahan: Sistem Penilaian Praktikum Otomatis & Gamifikasi

Aplikasi GUI ini mengimplementasikan inovasi UI yang melampaui kriteria tugas:

1. **Smart Timer Sesi Praktikum**: Di halaman **Penilaian**, dosen dapat membuka pertemuan dan frontend memutar *stopwatch* secara dinamis (*real-time clock update*). Menghilangkan ketergantungan pencatatan waktu dengan alat konvensional.
2. **Sistem Rating Bintang (Evolusi Ceklis)**: Merubah desain input primitif *checkbox* menjadi komponen bintang interaktif (skala 1–5) dengan animasi mikro yang memberikan rasa apresiasi lebih bagi para mahasiswa.
3. **Dashboard Klasemen (Leaderboard) "Top 10"**: Menggabungkan konsep *Gamifikasi*, perolehan total bintang seluruh mahasiswa dihitung *real-time* dan ditampilkan secara estetik dengan elemen gradasi emas (medali 🥇, 🥈, 🥉) guna membangun atmosfer kompetitif antar mahasiswa.

---

## 🔐 Sistem Keamanan (Security) & JWT
*Frontend* mengintegrasikan proteksi alur masuk (Autentikasi). Setelah formulir Login disetujui, token *JWT* diinjeksi ke penyimpanan *local (`localStorage`)* browser. Setiap *request API* selanjutnya secara otomatis menyematkan header `X-Token`. Bila token dimanipulasi atau kadaluwarsa, *frontend* seketika menyuruh *browser* melakukan *redirect* kembali ke layar Login.

---

## 📦 Stack Teknologi

| Lapisan (Layer) | Teknologi Utama |
|-----------------|-----------------|
| **Web Server / Proxy** | Flask (Python 3.13) |
| **Templating Engine** | Jinja2 |
| **Logika UI Klien** | ES6 Vanilla JavaScript |
| **Desain Styling UI** | TailwindCSS v3 (via CDN) |
| **Komponen Interaktif** | TomSelect (Dropdown Interaktif) |
