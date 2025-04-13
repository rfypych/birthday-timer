# Modul Notifikasi

Modul ini menangani sistem notifikasi ulang tahun dan pengaturan startup Windows.

## Kelas BirthdayNotifier

Kelas utama untuk mengelola notifikasi dan pengaturan sistem.

### Metode:

1. `show_notification(title, message, icon_path=None, duration=10)`
   - Menampilkan notifikasi desktop Windows
   - Parameters:
     * title: Judul notifikasi
     * message: Isi pesan notifikasi
     * icon_path: Path ke file ikon (opsional)
     * duration: Durasi notifikasi dalam detik

2. `check_birthdays(birthdays, days_threshold=7)`
   - Memeriksa ulang tahun yang akan datang
   - Parameters:
     * birthdays: List data ulang tahun
     * days_threshold: Batas hari untuk notifikasi (default 7)
   - Returns: List notifikasi yang perlu ditampilkan

3. `set_startup(app_path, app_name="BirthdayReminder")`
   - Mengatur aplikasi agar berjalan saat startup Windows
   - Parameters:
     * app_path: Path lengkap ke aplikasi
     * app_name: Nama aplikasi di registry

4. `remove_startup(app_name="BirthdayReminder")`
   - Menghapus aplikasi dari startup Windows
   - Parameters:
     * app_name: Nama aplikasi di registry

5. `create_birthday_icon(output_path, size=256)`
   - Membuat ikon kue ulang tahun untuk notifikasi
   - Parameters:
     * output_path: Path output untuk file ikon
     * size: Ukuran ikon dalam pixel

### Fitur:
- Notifikasi desktop Windows dengan ikon kustom
- Pengaturan autostart Windows
- Sistem reminder untuk ulang tahun yang akan datang
- Pengelolaan notifikasi harian

### Penggunaan

```python
# Inisialisasi notifier
notifier = BirthdayNotifier()

# Tampilkan notifikasi
notifier.show_notification(
    "Selamat Ulang Tahun!",
    "Hari ini adalah ulang tahun seseorang!",
    "path/to/icon.ico"
)

# Cek ulang tahun yang akan datang
notifications = notifier.check_birthdays(birthdays_list)
```