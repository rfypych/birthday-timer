# Aplikasi Pengingat Ulang Tahun dengan Gaya Pixel Art

Aplikasi pengingat ulang tahun bergaya pixel art untuk mengingat dan mengelola informasi ulang tahun orang-orang tersayang. Dibuat khusus untuk Aira Jesslyn Seniara.

## Fitur

- ✨ Antarmuka bergaya pixel art dengan warna pastel yang menarik
- 🎂 Menambah, mengedit, dan menghapus data ulang tahun
- 🔔 Notifikasi sistem untuk ulang tahun yang akan datang
- 📅 Tampilan daftar ulang tahun dengan warna yang menunjukkan kedekatan waktu
- 🚀 Opsi untuk menjalankan aplikasi saat Windows startup

## Instalasi

1. Pastikan Python 3.6 atau yang lebih baru sudah terinstal di komputer Anda
2. Clone atau download repository ini
3. Instal dependensi yang dibutuhkan:

```
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```
python main.py
```

## Penggunaan

1. **Menambah Ulang Tahun**:
   - Isi nama dan tanggal ulang tahun di form yang tersedia
   - Klik tombol "Simpan" untuk menyimpan data

2. **Mengedit Ulang Tahun**:
   - Pilih data ulang tahun yang ingin diedit dari daftar
   - Klik tombol "Edit" dan ubah informasi yang diinginkan

3. **Menghapus Ulang Tahun**:
   - Pilih data ulang tahun yang ingin dihapus dari daftar
   - Klik tombol "Hapus" dan konfirmasi penghapusan

4. **Mengaktifkan Notifikasi saat Startup**:
   - Klik tombol "Jalankan Saat Startup" untuk menambahkan aplikasi ke startup Windows
   - Aplikasi akan berjalan otomatis saat Windows startup

## Kustomisasi

Anda dapat mengubah berbagai aspek aplikasi dengan memodifikasi konstanta di awal file `main.py`:

- Ubah skema warna dengan mengganti nilai warna HEX
- Ubah ukuran jendela dengan memodifikasi nilai WIDTH dan HEIGHT
- Ubah gaya font dengan mengganti nilai FONT_STYLE

## Informasi Teknis

- Bahasa: Python 3
- UI Framework: Tkinter
- Penyimpanan Data: JSON
- Notifikasi: win10toast (Windows 10/11)

## Lisensi

Proyek ini merupakan proyek pribadi dan ditujukan untuk penggunaan pribadi oleh Aira Jesslyn Seniara. Dilarang mendistribusikan tanpa izin. 