# Modul Aplikasi Utama

## Birthday Timer v2.0
Aplikasi pengingat ulang tahun dengan tampilan menarik dan fitur lengkap.  
Dibuat oleh: Rofikul Huda

## Fitur Utama

### 1. Manajemen Data Ulang Tahun
- Tambah, edit, dan hapus data
- Pengaturan prioritas
- Validasi input data
- Import/export data

### 2. Tampilan Countdown
- Countdown realtime untuk ulang tahun prioritas
- Update otomatis setiap detik
- Tampilan jam dan tanggal
- Animasi dan hiasan visual

### 3. Kalender Interaktif
- Visualisasi tanggal ulang tahun
- Penanda khusus untuk hari ini dan ulang tahun prioritas
- Detail informasi saat tanggal dipilih
- Warna berbeda untuk kategori berbeda

### 4. Sistem Notifikasi
- Notifikasi desktop untuk ulang tahun yang akan datang
- Pengaturan waktu notifikasi per data
- Notifikasi otomatis saat startup
- Ikon kue ulang tahun kustom

### 5. Pengaturan Aplikasi
- Autostart Windows
- Backup dan restore data
- Pengaturan tampilan
- Penyimpanan preferensi

### 6. Fitur Testing
- Test sistem notifikasi
- Test validasi input
- Test operasi data
- Dokumentasi pengujian

## Teknologi yang Digunakan
- Python dengan Tkinter untuk UI
- Sistem notifikasi Windows (win10toast)
- JSON untuk penyimpanan data
- Pillow untuk manipulasi gambar
- tkcalendar untuk widget kalender

## Requirements
- Windows OS
- Python 3.x
- Package yang dibutuhkan:
  * win10toast
  * pillow
  * tkcalendar

## Struktur Aplikasi

### Kelas Utama: BirthdayReminderApp
Metode-metode utama:
1. `create_ui()`: Membuat antarmuka utama
2. `update_time_and_countdown()`: Update timer realtime
3. `add_birthday()`: Menambah data baru
4. `edit_birthday()`: Mengedit data existing
5. `delete_birthday()`: Menghapus data
6. `check_notifications()`: Mengecek dan menampilkan notifikasi
7. `create_calendar_tab()`: Membuat tab kalender
8. `create_settings_tab()`: Membuat tab pengaturan
9. `create_testing_tab()`: Membuat tab testing
10. `create_docs_tab()`: Membuat tab dokumentasi

### Penyimpanan Data
- Format: JSON
- Lokasi: birthdays.json
- Fields:
  * id: ID unik
  * name: Nama
  * date: Tanggal lahir
  * time: Waktu notifikasi
  * priority: Status prioritas

## Kontak
Dikembangkan oleh Rofikul Huda

# Dokumentasi Modul App

Modul ini berisi implementasi utama aplikasi pengingat ulang tahun, termasuk kelas-kelas dialog dan fungsi-fungsi pendukung.

## Kelas BaseDialog

Kelas dasar untuk membuat dialog modal dalam aplikasi.

### Properti

- `parent`: Widget parent untuk dialog
- `title`: Judul dialog
- `callback`: Fungsi yang dipanggil saat dialog ditutup
- `ok_text`: Teks untuk tombol OK
- `result`: Hasil dari dialog

### Metode

#### `__init__(parent, title, callback=None, ok_text="OK", width=540, height=380)`
- Inisialisasi dialog baru
- **Parameters:**
  - parent: Widget parent
  - title: Judul dialog
  - callback: Fungsi callback (opsional)
  - ok_text: Teks tombol OK
  - width: Lebar dialog
  - height: Tinggi dialog

#### `body(master)`
- Membuat body dialog
- **Parameters:**
  - master: Frame parent untuk body
- **Returns:** Widget yang akan mendapat fokus awal

#### `buttonbox()`
- Membuat area tombol dialog

#### `ok(event=None)`
- Handler untuk tombol OK
- Memvalidasi input dan memanggil callback

#### `cancel(event=None)`
- Handler untuk tombol Cancel
- Menutup dialog tanpa menyimpan

## Kelas AddBirthdayDialog

Dialog untuk menambah data ulang tahun baru.

### Properti

- `name_entry`: Entry untuk nama
- `date_entry`: Entry untuk tanggal
- `hour_var`: Variable untuk jam
- `minute_var`: Variable untuk menit
- `priority_var`: Variable untuk status prioritas

### Metode

#### `validate()`
- Memvalidasi input form
- **Returns:** Boolean validitas input

#### `apply()`
- Memproses dan menyimpan data ulang tahun baru

## Kelas EditBirthdayDialog

Dialog untuk mengedit data ulang tahun yang ada.

### Properti

- `initial_data`: Data awal yang akan diedit
- Form fields sama dengan AddBirthdayDialog

### Metode

#### `validate()`
- Memvalidasi perubahan data
- **Returns:** Boolean validitas input

#### `apply()`
- Menyimpan perubahan data

## Kelas ExportDialog

Dialog untuk mengekspor data ulang tahun.

### Properti

- `data`: Data yang akan diekspor
- `add_metadata_var`: Opsi untuk menambah metadata

### Metode

#### `validate()`
- Memvalidasi lokasi ekspor
- **Returns:** Boolean sukses/gagal

#### `apply()`
- Melakukan ekspor data ke file JSON

## Fungsi Utilitas

### `create_data_file()`
- Membuat file data JSON jika belum ada
- **Returns:** None

### `adjust_color(hex_color, amount)`
- Menyesuaikan warna hex dengan menambah/mengurangi nilai RGB
- **Parameters:**
  - hex_color: Warna dalam format hex
  - amount: Jumlah penyesuaian (-255 sampai 255)
- **Returns:** Warna hex yang disesuaikan